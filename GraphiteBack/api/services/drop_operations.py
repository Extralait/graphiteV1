from api.models import Drop, OwnerDrop


def sell_drop(drop_id, count, user):
    drop = Drop.objects.get(pk=drop_id)
    sell_count = drop.sell_count
    owner = OwnerDrop.objects.get(drop_id=drop_id).drop_owner.pk

    try:
        user_drop_id = OwnerDrop.objects.get(drop__parent_id=drop_id, drop_owner_ШВ=user).drop.pk
        user_drop = Drop.objects.get(pk=user_drop_id)
    except OwnerDrop.DoesNotExist:
        user_drop = None

    if sell_count > count:
        drop.sell_count -= count
        drop.save()
    else:
        drop.sell_count = 0
        drop.save()
        count = sell_count

    if user_drop:
        user_drop.sell_count += count
        user_drop.save()
        customer_drop = user_drop_id
    else:
        drop.pk = None
        drop.sell_count = count
        drop.parent_id = drop_id
        drop.save()
        new_drop_id = drop.pk
        OwnerDrop.objects.create(
            drop_owner_id=user,
            drop_id=new_drop_id,
        )
        customer_drop = new_drop_id

    return count, user, owner, customer_drop
