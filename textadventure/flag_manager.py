class FlagManager:
    def set_flag(self, flags, flag):
        if flag not in flags:
            flags.add(flag)

    def has_flag(self, game, flag):
        if flag in game.flags:
            return True
        return False
            
    def has_flags(self, game, flags):    
        for flag in flags:
            if self.has_flag(game, flag):
                return True
        return False
    
    def no_flags(self, game, flags):
        for flag in flags:
            if self.has_flag(game, flag):
                return False
        return False