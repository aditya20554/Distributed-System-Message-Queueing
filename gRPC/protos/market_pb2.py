# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: market.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmarket.proto\x12\x0bmarketplace\"K\n\x08Response\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0c\n\x04uuid\x18\x03 \x01(\t\x12\x0f\n\x07item_id\x18\x04 \x01(\x05\"\xca\x01\n\x04Item\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\'\n\x08\x63\x61tegory\x18\x03 \x01(\x0e\x32\x15.marketplace.Category\x12\x10\n\x08quantity\x18\x04 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\r\n\x05price\x18\x06 \x01(\x02\x12\x16\n\x0eseller_address\x18\x07 \x01(\t\x12\x0e\n\x06rating\x18\x08 \x01(\x02\x12\x10\n\x08rated_by\x18\t \x03(\t\x12\x0f\n\x07ratings\x18\n \x03(\x05\"\'\n\x06Seller\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\"<\n\x15RegisterSellerRequest\x12#\n\x06seller\x18\x01 \x01(\x0b\x32\x13.marketplace.Seller\",\n\x08ItemList\x12 \n\x05items\x18\x01 \x03(\x0b\x32\x11.marketplace.Item\"@\n\x0fSellItemRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x1f\n\x04item\x18\x02 \x01(\x0b\x32\x11.marketplace.Item\"S\n\x11UpdateItemRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07item_id\x18\x02 \x01(\x05\x12\x10\n\x08quantity\x18\x03 \x01(\x05\x12\r\n\x05price\x18\x04 \x01(\x02\"2\n\x11\x44\x65leteItemRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07item_id\x18\x02 \x01(\x05\")\n\x19\x44isplaySellerItemsRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"J\n\x11SearchItemRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\'\n\x08\x63\x61tegory\x18\x02 \x01(\x0e\x32\x15.marketplace.Category\"J\n\x0e\x42uyItemRequest\x12\x15\n\rbuyer_address\x18\x01 \x01(\t\x12\x0f\n\x07item_id\x18\x02 \x01(\x05\x12\x10\n\x08quantity\x18\x03 \x01(\x05\"9\n\x0fWishListRequest\x12\x15\n\rbuyer_address\x18\x01 \x01(\t\x12\x0f\n\x07item_id\x18\x02 \x01(\x05\"I\n\x0fRateItemRequest\x12\x15\n\rbuyer_address\x18\x01 \x01(\t\x12\x0f\n\x07item_id\x18\x02 \x01(\x05\x12\x0e\n\x06rating\x18\x03 \x01(\x05\"(\n\x13NotificationRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\"P\n\x14NotificationResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\'\n\x0cupdated_item\x18\x02 \x01(\x0b\x32\x11.marketplace.Item*=\n\x08\x43\x61tegory\x12\x0f\n\x0b\x45LECTRONICS\x10\x00\x12\x0b\n\x07\x46\x41SHION\x10\x01\x12\n\n\x06OTHERS\x10\x02\x12\x07\n\x03\x41NY\x10\x03\x32\xf5\x05\n\x12MarketplaceService\x12M\n\x0eRegisterSeller\x12\".marketplace.RegisterSellerRequest\x1a\x15.marketplace.Response\"\x00\x12\x41\n\x08SellItem\x12\x1c.marketplace.SellItemRequest\x1a\x15.marketplace.Response\"\x00\x12\x45\n\nUpdateItem\x12\x1e.marketplace.UpdateItemRequest\x1a\x15.marketplace.Response\"\x00\x12\x45\n\nDeleteItem\x12\x1e.marketplace.DeleteItemRequest\x1a\x15.marketplace.Response\"\x00\x12U\n\x12\x44isplaySellerItems\x12&.marketplace.DisplaySellerItemsRequest\x1a\x15.marketplace.ItemList\"\x00\x12\x45\n\nSearchItem\x12\x1e.marketplace.SearchItemRequest\x1a\x15.marketplace.ItemList\"\x00\x12?\n\x07\x42uyItem\x12\x1b.marketplace.BuyItemRequest\x1a\x15.marketplace.Response\"\x00\x12\x46\n\rAddToWishList\x12\x1c.marketplace.WishListRequest\x1a\x15.marketplace.Response\"\x00\x12\x41\n\x08RateItem\x12\x1c.marketplace.RateItemRequest\x1a\x15.marketplace.Response\"\x00\x12U\n\x0cNotifyClient\x12 .marketplace.NotificationRequest\x1a!.marketplace.NotificationResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'market_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CATEGORY']._serialized_start=1116
  _globals['_CATEGORY']._serialized_end=1177
  _globals['_RESPONSE']._serialized_start=29
  _globals['_RESPONSE']._serialized_end=104
  _globals['_ITEM']._serialized_start=107
  _globals['_ITEM']._serialized_end=309
  _globals['_SELLER']._serialized_start=311
  _globals['_SELLER']._serialized_end=350
  _globals['_REGISTERSELLERREQUEST']._serialized_start=352
  _globals['_REGISTERSELLERREQUEST']._serialized_end=412
  _globals['_ITEMLIST']._serialized_start=414
  _globals['_ITEMLIST']._serialized_end=458
  _globals['_SELLITEMREQUEST']._serialized_start=460
  _globals['_SELLITEMREQUEST']._serialized_end=524
  _globals['_UPDATEITEMREQUEST']._serialized_start=526
  _globals['_UPDATEITEMREQUEST']._serialized_end=609
  _globals['_DELETEITEMREQUEST']._serialized_start=611
  _globals['_DELETEITEMREQUEST']._serialized_end=661
  _globals['_DISPLAYSELLERITEMSREQUEST']._serialized_start=663
  _globals['_DISPLAYSELLERITEMSREQUEST']._serialized_end=704
  _globals['_SEARCHITEMREQUEST']._serialized_start=706
  _globals['_SEARCHITEMREQUEST']._serialized_end=780
  _globals['_BUYITEMREQUEST']._serialized_start=782
  _globals['_BUYITEMREQUEST']._serialized_end=856
  _globals['_WISHLISTREQUEST']._serialized_start=858
  _globals['_WISHLISTREQUEST']._serialized_end=915
  _globals['_RATEITEMREQUEST']._serialized_start=917
  _globals['_RATEITEMREQUEST']._serialized_end=990
  _globals['_NOTIFICATIONREQUEST']._serialized_start=992
  _globals['_NOTIFICATIONREQUEST']._serialized_end=1032
  _globals['_NOTIFICATIONRESPONSE']._serialized_start=1034
  _globals['_NOTIFICATIONRESPONSE']._serialized_end=1114
  _globals['_MARKETPLACESERVICE']._serialized_start=1180
  _globals['_MARKETPLACESERVICE']._serialized_end=1937
# @@protoc_insertion_point(module_scope)
