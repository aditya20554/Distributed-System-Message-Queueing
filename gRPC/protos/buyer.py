import grpc
import market_pb2 as mp
import market_pb2_grpc as mpg
import threading
# buyer_address = "localhost:50051"

class BuyerClient:
    def __init__(self, buyer_id):
        self.buyer_id = buyer_id
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = mpg.MarketplaceServiceStub(self.channel)
        self.buyer_address = f"localhost:{buyer_id}" 

    def search_items(self):
        try:
            
            item_name = input("Enter the item name to search for (leave blank for all items): ").lower()
            category_input = input("Enter category (ELECTRONICS, FASHION, OTHERS, ANY): ").upper()

            
            valid_categories = ['ELECTRONICS', 'FASHION', 'OTHERS', 'ANY']
            if category_input in valid_categories:
                category = getattr(mp.Category, category_input) if category_input != 'ANY' else mp.ANY
            else:
                raise ValueError("Invalid category. Please choose from ELECTRONICS, FASHION, OTHERS, ANY.")

            
            response = self.stub.SearchItem(mp.SearchItemRequest(name=item_name, category=category))

            
            print("Buyer prints:")
            for item in response.items:
                print("–")
                print(f"Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, Category: {mp.Category.Name(item.category)},")
                print(f"Description: {item.description}\nQuantity Remaining: {item.quantity}\nRating: {item.rating} / 5  |  Seller: {item.seller_address}")
                print("-")

        except grpc.RpcError as e:
            print(f"An RPC error occurred: {e.code()} {e.details()}")
        except ValueError as e:
            print(str(e))
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def buy_item(self, item_id, quantity):
        try:
            response = self.stub.BuyItem(mp.BuyItemRequest(
                item_id=item_id,
                quantity=quantity,
                buyer_address=self.buyer_address
            ))

            print(f"Buy Item response: {response.message}")
            return response.success
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


    def add_to_wishlist(self, item_id):
        try:
            response = self.stub.AddToWishList(mp.WishListRequest(
                item_id=item_id,
                buyer_address=self.buyer_address 
            ))

            print(f"AddToWishList response: {response.message}")
            return response.success
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


    def rate_item(self, item_id, rating):
        try:
            response = self.stub.RateItem(mp.RateItemRequest(
                item_id=item_id,
                rating=rating,
                buyer_address=self.buyer_address  
            ))

            print(f"Rate Item response: {response.message}")
            return response.success
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

        

def listen_for_notifications(buyer_id):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = mpg.MarketplaceServiceStub(channel)
        try:
            
            for notification in stub.NotifyClient(mp.NotificationRequest(client_id=buyer_id)):
                print("\n#######\nNotification:\n")
                print(f"Item ID: {notification.updated_item.id}, Price: ${notification.updated_item.price}, "
                    f"Name: {notification.updated_item.name}, Category: {mp.Category.Name(notification.updated_item.category)}")
                print(f"Description: {notification.updated_item.description}\nQuantity Remaining: {notification.updated_item.quantity}\n"
                    f"Seller: {notification.updated_item.seller_address}\nRating: {notification.updated_item.rating} / 5\n")
                print("#######\n")
        except grpc.RpcError as e:
            print(f"An error occurred while listening for notifications: {e}")

if __name__ == '__main__':
    buyer_id = input("Enter a unique identifier for the buyer: ")
    buyer_client = BuyerClient(buyer_id)
    threading.Thread(target=listen_for_notifications, args=(buyer_id,), daemon=True).start()
    while True:
        print("\nChoose an option:")
        print("1. Search for items")
        print("2. Buy an item")
        print("3. Add an item to wishlist")
        print("4. Add rating")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            buyer_client.search_items()
        elif choice == '2':
            item_id = int(input("Enter the item ID to buy: "))
            quantity = int(input("Enter the quantity to buy: "))
            success = buyer_client.buy_item(item_id, quantity)
            if success:
                print("Purchase successful.")
            else:
                print("Purchase failed.")
        elif choice == '3':
            item_id = int(input("Enter the item ID to add to wishlist: "))
            success = buyer_client.add_to_wishlist(item_id)
            if success:
                print("Item successfully added to wishlist.")
            else:
                print("Failed to add item to wishlist.")

        elif choice == '4':  
            item_id = int(input("Enter the item ID to rate: "))
            rating = int(input("Enter your rating (1-5): "))
            if rating < 1 or rating > 5:
                print("Invalid rating. Ratings should be between 1 to 5.")
            else:
                success = buyer_client.rate_item(item_id, rating)
                if success:
                    print("Rating submitted successfully.")
                else:
                    print("Failed to submit rating.")
                    
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    
