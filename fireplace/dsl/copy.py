from hearthstone.enums import CardType, GameTag

from ..logging import log
from .lazynum import LazyValue


class Copy(LazyValue):
    """
    Lazily return a list of copies of the target
    """

    def __init__(self, selector):
        self.selector = selector

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.selector)

    def copy(self, source, entity):
        """
        Return a copy of \a entity
        """
        log.info("Creating a copy of %r", entity)
        new_entity = source.controller.card(entity.id, source)
        if entity.custom_card:
            new_entity.custom_card = True
            new_entity.create_custom_card = entity.create_custom_card
            new_entity.create_custom_card(new_entity)
        return new_entity

    def evaluate(self, source) -> list[str]:
        if isinstance(self.selector, LazyValue):
            entity = self.selector.evaluate(source)
            entities = [entity] if entity else []
        else:
            entities = self.selector.eval(source.game, source)

        return [self.copy(source, e) for e in entities]


class ExactCopy(Copy):
    """
    Lazily create an exact copy of the target.
    An exact copy will include buffs and all tags.
    """

    def __init__(self, selector, id=None):
        self.id = id
        self.selector = selector

    def copy(self, source, entity):
        ret = super().copy(source, entity)
        if self.id:
            ret = source.controller.card(self.id, source)
        for buff in entity.buffs:
            # Recreate the buff stack
            new_buff = source.controller.card(buff.id)
            new_buff.source = buff.source
            attributes = [
                "atk",
                "max_health",
                "_xatk",
                "_xhealth",
                "_xcost",
                "store_card",
            ]
            for attribute in attributes:
                if hasattr(buff, attribute):
                    setattr(new_buff, attribute, getattr(buff, attribute))
            new_buff.apply(ret)
            if buff in source.game.active_aura_buffs:
                new_buff.tick = buff.tick
                source.game.active_aura_buffs.append(new_buff)
        if entity.type == CardType.MINION:
            for k in entity.silenceable_attributes:
                v = getattr(entity, k)
                setattr(ret, k, v)
            ret.silenced = entity.silenced
            ret.damage = entity.damage
        return ret


class KeepMagneticCopy(Copy):
    """
    Kangor's Endless Army
    They keep any <b>Magnetic</b> upgrades
    """

    def __init__(self, selector, id=None):
        self.id = id
        self.selector = selector

    def copy(self, source, entity):
        ret = super().copy(source, entity)
        if self.id:
            ret = source.controller.card(self.id, source)
        for buff in entity.buffs:
            if getattr(buff.source, "has_magnetic", False):
                buff.source.buff(ret, buff.id, atk=buff.atk, max_health=buff.max_health)
        return ret


class RebornCopy(Copy):
    def copy(self, source, entity):
        ret = super().copy(source, entity)
        ret.reborn = False
        ret.set_current_health(1)
        return ret
