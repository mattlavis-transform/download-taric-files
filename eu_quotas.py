from classes.quota_handler import QuotaHandler

quotaHandler = QuotaHandler()
quotaHandler.get_quotas()
quotaHandler.get_quota_balances()
quotaHandler.assign_quota_balances()

quotaHandler.get_measures()

quotaHandler.write_excel()
