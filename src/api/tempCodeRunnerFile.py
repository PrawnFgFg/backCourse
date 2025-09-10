# ter.patch('/{hotel_id}/rooms/{room_id}')
# async def patch_update_room(
#     db: DBDep,
#     hotel_id: int,
#     room_id: int,
#     patch_schema: RoomPatchRequest,
# ):
#     room_data = RoomPatch(hotel_id=hotel_id, **patch_schema.model_dump(exclude_unset=True))
#     edited_room = await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
    
#     room_facilities_models = await db.room_facility.get_filtered(rooms_id=room_id)
    
#     current_facilities = []
#     for model in room_facilities_models:
#         id_facility = model.model_dump()['facility_id']
#         current_facilities.append(id_facility)
    
#     facilities_to_add = patch_schema.model_dump().get("facilities_ids_to_add", None)
    
#     if facilities_to_add:
#         facility_to_add_request = []
#         for fac in facilities_to_add:
#             if fac not in current_facilities:
#                 facility_to_add_request.append(fac)
        
#         models_rmfac = [RoomFacilityAdd(rooms_id=edited_room.id, facility_id=f_id) for f_id in facility_to_add_request]
#         await db.room_facility.add_bulk(models_rmfac)
    
    
#     facilities_to_del = patch_schema.model_dump().get("facilities_ids_to_del", None)
#     if facilities_to_del:
        
#         await db.room_facility.delete_bulk_for_id(room_id=room_id, ids_facilities=facilities_to_del)
    
#     await db.room_facility.facility_ids_to_del_and_add(
#         db=db,
        
#     )
    
#     room_facilities_models = await db.room_facility.get_filtered(rooms_id=room_id)
        
#     models_rmfac = db.room_facility.get_facilities_to_add(room_facilities_models, patch_schema, edited_room)
#     await db.room_facility.add_bulk(models_rmfac)
    
#     fac_to_del = db.room_facility.get_facilities_to_del(patch_schema)
#     await db.room_facility.delete_bulk_for_id(room_id=room_id, ids_facilities=fac_to_del)

#     await db.session.commit()
#     return edited_room