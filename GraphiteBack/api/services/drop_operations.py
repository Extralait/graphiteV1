from api.models import Drop, OwnerDrop


def sell_drop(drop_id, count, user):
    drop = Drop.objects.get(pk=drop_id)
    sell_count = drop.sell_count

    try:
        user_drop_id = OwnerDrop.objects.get(drop__parent_id=drop_id, drop_owner=user).id
        user_drop = Drop.objects.get(pk = user_drop_id)
    except OwnerDrop.DoesNotExist:
        user_drop=None

    if sell_count > count:
        drop.sell_count -= count
        drop.save()

        if user_drop:
            user_drop.sell_count += count
            user_drop.save()
        else:
            drop.pk = None
            drop.sell_count = count
            drop.parent_id = drop_id
            drop.save()
            new_drop_id = drop.pk
            OwnerDrop.objects.create(
                drop_owner_id = user,
                drop_id = new_drop_id,
            )
        return count

    else:
        if user_drop:
            user_drop.sell_count += sell_count
            user_drop.parent = None
            user_drop.save()
            drop.delete()
        else:
            owner_drop = OwnerDrop.objects.get(drop = drop_id)
            owner_drop.drop_owner_id = user
            owner_drop.save()

        return sell_count



