from concurrent import futures
import queue
import grpc
import market_pb2 as mp
import market_pb2_grpc as mpg

class MarketplaceService(mpg.MarketplaceServiceServicer):

    def __init__(self):
        self.registered_sellers = {}
        self.items = {}
        self.wishlist = {}
        self.next_item_id = 1
        self.client_streams = {}
        self.notification_queues = {}

    def RegisterSeller(self, request, context):
        seller_info = request.seller
        print(f"Seller join request from {seller_info.address}, uuid = {seller_info.uuid}")


        if seller_info.uuid in self.registered_sellers:
            return mp.Response(success=False, message='FAIL: Seller already registered')


        self.registered_sellers[seller_info.uuid] = {'address': seller_info.address}
        print("Registered sellers:", self.registered_sellers)  
        return mp.Response(success=True, message='SUCCESS')


    
    def SellItem(self, request, context):
        global next_item_id
        print(f"Sell Item request from {request.uuid}")
        if request.uuid not in self.registered_sellers:
            return mp.Response(success=False, message='FAIL: Seller not registered')

        item = request.item
        item.id = self.next_item_id  
        self.next_item_id += 1  

        self.items[item.id] = item  
        return mp.Response(success=True, message='SUCCESS', item_id=item.id) 


    
    def UpdateItem(self, request, context):
        print(f"Update Item {request.item_id}, request from {request.uuid}")
        try:
            if request.uuid not in self.registered_sellers:
                return mp.Response(success=False, message='FAIL: Seller not registered')
            if request.item_id not in self.items:
                return mp.Response(success=False, message='FAIL: Item not found')

            item = self.items[request.item_id]
            item.price = request.price
            item.quantity = request.quantity

            # if request.item_id in self.wishlist:
                
            #     notification_message = "The Following Item has been updated:"
            #     for buyer_address in self.wishlist[request.item_id]:
                    
            #         self.add_notification_for_client(
            #             buyer_address,
            #             notification_message,
            #             updated_item=item
            #         )
            self.NotifyWishlistedBuyers(request.item_id, self.items[request.item_id])

            return mp.Response(success=True, message='SUCCESS')
        except Exception as e:
            print(f"An error occurred while updating item: {str(e)}")
            return mp.Response(success=False, message=f'FAIL: {str(e)}')



    def DeleteItem(self, request, context):
        print(f"Delete Item {request.item_id}, request from {request.uuid}")
        try:
            if request.uuid not in self.registered_sellers:
                return mp.Response(success=False, message='FAIL: Seller not registered')
            if request.item_id not in self.items:
                return mp.Response(success=False, message='FAIL: Item not found')

            
            del self.items[request.item_id]
            print(f"Delete Item {request.item_id} request from {self.registered_sellers[request.uuid]['address']}")
            return mp.Response(success=True, message='SUCCESS')
        except Exception as e:
            print(f"An error occurred while deleting item: {str(e)}")
            return mp.Response(success=False, message=f'FAIL: {str(e)}')



    def DisplaySellerItems(self, request, context):
        seller_uuid = request.uuid
        if seller_uuid in self.registered_sellers:
            seller_address = self.registered_sellers[seller_uuid]['address']
            seller_items = [item for item in self.items.values() if item.seller_address == seller_address]
            return mp.ItemList(items=seller_items)
        else:
            return mp.ItemList(items=[])
    
    
    def SearchItem(self, request, context):
        search_results = []
        for item in self.items.values():
            if not request.name or request.name.lower() in item.name.lower():
                if request.category == mp.ANY or request.category == item.category:
                    search_results.append(item)
        print(f"Search request for Item name: {request.name}, Category: {mp.Category.Name(request.category)}")
        return mp.ItemList(items=search_results)

    def BuyItem(self, request, context):
        try:
            if request.item_id not in self.items:
                return mp.Response(success=False, message='FAIL: Invalid item ID')

            item = self.items[request.item_id]
            if item.quantity < request.quantity:
                return mp.Response(success=False, message='FAIL: Not enough stock available')

            item.quantity -= request.quantity
            seller_uuid = None
            for seller_id, seller_info in self.registered_sellers.items():
                if seller_info['address'] == item.seller_address:
                    seller_uuid = seller_id
                    break

            if seller_uuid:
                notification_message = f"Item {request.item_id} has been purchased by {request.buyer_address}. Remaining quantity: {item.quantity}"
                self.add_notification_for_client(seller_uuid, notification_message, updated_item=item)

            print(f"Buy request {request.quantity} of item {request.item_id}, from {request.buyer_address}")
            return mp.Response(success=True, message='SUCCESS')
        
        except Exception as e:
            print(f"An error occurred while buying item: {str(e)}")
            return mp.Response(success=False, message=f'FAIL: {str(e)}')


    def AddToWishList(self, request, context):
        
        if request.item_id not in self.wishlist:
            self.wishlist[request.item_id] = set()
    
        if request.buyer_address not in self.wishlist[request.item_id]:
            self.wishlist[request.item_id].add(request.buyer_address)
            
            if request.buyer_address not in self.notification_queues:
                self.notification_queues[request.buyer_address] = queue.Queue()
            print(f"Wishlist request of item {request.item_id}, from {request.buyer_address}")
            return mp.Response(success=True, message='SUCCESS')
        else:
            
            return mp.Response(success=False, message='FAIL: Item already wishlisted')




    def RateItem(self, request, context):
        
        if request.item_id not in self.items:
            return mp.Response(success=False, message='FAIL: Item not found')

        item = self.items[request.item_id]
        
        
        if request.buyer_address in item.rated_by:
            return mp.Response(success=False, message='FAIL: Buyer has already rated this item')

        
        item.rated_by.append(request.buyer_address)
        item.ratings.append(request.rating)  

        
        item.ratings.append(request.rating)
        total_ratings = sum(item.ratings)
        item.rating = total_ratings / len(item.ratings)


        print(f"{request.buyer_address} rated item {request.item_id} with {request.rating} stars.")
        return mp.Response(success=True, message='SUCCESS')
    
    def NotifyWishlistedBuyers(self, item_id, updated_item):
        
        if item_id in self.wishlist:
            
            for buyer_address in self.wishlist[item_id]:
                if buyer_address in self.notification_queues:
                    
                    notification_message = mp.NotificationResponse(
                        message="An item you have wishlisted has been updated.",
                        updated_item=updated_item
                    )
                    
                    self.notification_queues[buyer_address].put(notification_message)

        
    def NotifyClient(self, request, context):
        
        if request.client_id not in self.notification_queues:
            self.notification_queues[request.client_id] = queue.Queue()

        
        notifications = self.notification_queues[request.client_id]

        
        try:
            while True:
                try:
                    
                    notification_response = notifications.get(timeout=10)
                    yield notification_response
                except queue.Empty:
                    
                    continue
        finally:
            
            del self.notification_queues[request.client_id]
    
    def add_notification_for_client(self, client_id, message, updated_item=None):
       
        notification_response = mp.NotificationResponse(
            message=message,
            updated_item=updated_item if updated_item else mp.Item()
        )

        
        if client_id in self.notification_queues:
            self.notification_queues[client_id].put(notification_response)
            

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mpg.add_MarketplaceServiceServicer_to_server(MarketplaceService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on '50051'")
    server.wait_for_termination()

if __name__ == '__main__':
    server()
