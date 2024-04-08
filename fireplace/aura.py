from .logging import log
from .managers import CardManager


class AuraBuff:
    def __init__(self, source, entity):
        self.source = source
        self.entity = entity
        self.tags = CardManager(self)

    def __repr__(self):
        return "<AuraBuff %r -> %r>" % (self.source, self.entity)

    def update_tags(self, tags):
        self.tags.update(tags)
        self.tick = self.source.game.tick

    def remove(self):
        log.info("Destroying %r", self)
        self.entity.slots.remove(self)
        self.source.game.active_aura_buffs.remove(self)

    def _getattr(self, attr, i):
        value = getattr(self, attr, 0)
        if callable(value):
            return value(self.entity, i)
        return i + value


class Refresh:
    """
    Refresh a buff or a set of tags on an entity
    """

    def __init__(self, selector, tags=None, buff=None, priority=50):
        self.selector = selector
        self.tags = tags
        self.buff = buff
        self.priority = priority

    def trigger(self, source):
        entities = self.selector.eval(source.game, source)
        for entity in entities:
            if self.buff:
                entity.refresh_buff(source, self.buff)
            else:
                tags = {}
                for tag, value in self.tags.items():
                    if not isinstance(value, int) and not callable(value):
                        value = value.evaluate(source)
                    tags[tag] = value

                entity.refresh_tags(source, tags)

    def __repr__(self):
        return "Refresh(%r, %r, %r)" % (self.selector, self.tags or {}, self.buff or "")


class TargetableByAuras:
    def refresh_buff(self, source, id):
        for buff in self.buffs:
            if buff.source is source and buff.id == id:
                buff.tick = source.game.tick
                break
        else:
            log.info("Aura from %r buffs %r with %r", source, self, id)
            buff = source.buff(self, id)
            buff.tick = source.game.tick
            source.game.active_aura_buffs.append(buff)

    def refresh_tags(self, source, tags):
        for slot in self.slots:
            if slot.source is source:
                slot.update_tags(tags)
                break
        else:
            buff = AuraBuff(source, self)
            log.info("Creating %r", buff)
            buff.update_tags(tags)
            self.slots.append(buff)
            source.game.active_aura_buffs.append(buff)
