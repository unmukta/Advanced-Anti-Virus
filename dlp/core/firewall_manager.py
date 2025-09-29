class FirewallManager:
    def __init__(self):
        self.rules = []
    
    def add_rule(self, rule_config):
        \"\"\"Add firewall rule\"\"\"
        self.rules.append(rule_config)
        return {"status": "added", "rule": rule_config}
    
    def list_rules(self):
        \"\"\"List all firewall rules\"\"\"
        return self.rules
