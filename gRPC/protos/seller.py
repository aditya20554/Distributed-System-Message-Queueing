import grpc
import market_pb2 as mp
import market_pb2_grpc as mpg
import uuid
import threading

seller_address = "localhost:50051"
seller_uuid = str(uuid.uuid1())

def register_seller():
    channel = grpc.insecure_channel(seller_address)
    stub = mpg.MarketplaceServiceStub(channel)
    response = stub.RegisterSeller(mp.RegisterSellerRequest(
        seller=mp.Seller(uuid=seller_uuid, address=seller_address)
    ))
    print(f"Seller registration response: {response.message}")
    return response.success, seller_uuid

# def sell_item(seller_uuid):
#     try:
#         channel = grpc.insecure_channel(seller_address)
#         stub = mpg.MarketplaceServiceStub(channel)

#         item_id_input = input("Enter item ID: ")
#         name = input("Enter product name: ")
#         category_input = input("Enter category (ELECTRONICS, FASHION, OTHERS): ").upper()
#         quantity_input = int(input("Enter quantity: "))
#         description = input("Enter description: ")
#         price_input = float(input("Enter price per unit: "))

        
#         item = mp.Item(
#             id=int(item_id_input),
#             name=name,
#             category=getattr(mp.Category, category_input),
#             quantity=quantity_input,
#             description=description,
#             price=price_input,
#             seller_address=seller_address
#         )

        
#         response = stub.SellItem(mp.SellItemRequest(uuid=seller_uuid, item=item))
#         if response.success:
#             print(f"Sell Item response: SUCCESS")
#             return True, int(item_id_input)
#         else:
#             print(f"Sell Item response: FAIL")
#             return False, None
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return False, None

def sell_item(seller_uuid):
    try:
        channel = grpc.insecure_channel(seller_address)
        stub = mpg.MarketplaceServiceStub(channel)

        name = input("Enter product name: ").lower()
        category_input = input("Enter category (ELECTRONICS, FASHION, OTHERS): ").upper()
        quantity_input = int(input("Enter quantity: "))
        description = input("Enter description: ")
        price_input = float(input("Enter price per unit: "))

        item = mp.Item(
            name=name,
            category=getattr(mp.Category, category_input),
            quantity=quantity_input,
            description=description,
            price=price_input,
            seller_address=seller_address
        )

        response = stub.SellItem(mp.SellItemRequest(uuid=seller_uuid, item=item))
        if response.success:
            print(f"Sell Item response: SUCCESS, Item ID: {response.item_id}")
            return True, response.item_id
        else:
            print(f"Sell Item response: FAIL")
            return False, None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False, None

def update_item(seller_uuid):
    try:
        channel = grpc.insecure_channel(seller_address)
        stub = mpg.MarketplaceServiceStub(channel)

        item_id = int(input("Enter the item ID to update: "))
        new_price = float(input("Enter the new price: "))
        new_quantity = int(input("Enter the new quantity: "))
        response = stub.UpdateItem(mp.UpdateItemRequest(
            uuid=seller_uuid,
            item_id=item_id,
            price=new_price,
            quantity=new_quantity
        ))
        print(f"Update Item response: {response.message}")
        return response.success
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False



def delete_item(seller_uuid):
    try:
        channel = grpc.insecure_channel(seller_address)
        stub = mpg.MarketplaceServiceStub(channel)

        item_id = int(input("Enter the item ID to delete: "))

        response = stub.DeleteItem(mp.DeleteItemRequest(
            uuid=seller_uuid,
            item_id=item_id
        ))

        print(f"Delete Item response: {response.message}")
        return response.success
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


def display_seller_items():
    try:
        channel = grpc.insecure_channel(seller_address)
        stub = mpg.MarketplaceServiceStub(channel)
        response = stub.DisplaySellerItems(mp.DisplaySellerItemsRequest(uuid=seller_uuid))
        print("Seller prints:")
        print(len(response.items))
        for item in response.items:
            print("-")
            print(f"Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, Category: {mp.Category.Name(item.category)}")
            print(f"Description: {item.description}, Quantity Remaining: {item.quantity}")
            print(f"Seller: {item.seller_address}")
            print(f"Rating: {item.rating} / 5")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def listen_for_notifications():
    with grpc.insecure_channel(seller_address) as channel:
        stub = mpg.MarketplaceServiceStub(channel)
        try:
            for notification in stub.NotifyClient(mp.NotificationRequest(client_id=seller_uuid)):
                print("\n#######\nThe Following Item has been updated:\n")
                print(f"Item ID: {notification.updated_item.id}, Price: ${notification.updated_item.price}, "
                      f"Name: {notification.updated_item.name}, Category: {mp.Category.Name(notification.updated_item.category)}")
                print(f"Description: {notification.updated_item.description}\nQuantity Remaining: {notification.updated_item.quantity}\n"
                      f"Seller: {notification.updated_item.seller_address}\nRating: {notification.updated_item.rating} / 5\n")
                print("#######\n")
        except grpc.RpcError as e:
            print(f"An error occurred while listening for notifications: {e}")

if __name__ == '__main__':
    success, seller_uuid = register_seller()
    if success:
        print(f"Seller registered with UUID: {seller_uuid}")
        
        notification_thread = threading.Thread(target=listen_for_notifications, daemon=True)
        notification_thread.start()
        

        while True:
            print("\nChoose an option:")
            print("1. Sell an item")
            print("2. Update an item")
            print("3. Delete an item")
            print("4. Display all items")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                sell_success, item_id = sell_item(seller_uuid)
                if sell_success:
                    print(f"Item sold successfully with Item ID: {item_id}")
                else:
                    print("Failed to sell item.")
            elif choice == '2':
                update_success = update_item(seller_uuid)
                if update_success:
                    print("Item updated successfully.")
                else:
                    print("Failed to update item.")
            elif choice == '3':
                delete_success = delete_item(seller_uuid)
                if delete_success:
                    print("Item deleted successfully.")
                else:
                    print("Failed to delete item.")
            elif choice == '4':
                display_seller_items()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


