from PyQt5.QtWidgets import QWidget

from forms.ui_overviewpage import Ui_OverviewPage

class OverviewPage(QWidget, Ui_OverviewPage):
    """The overview page.

    It presents the current wallets (lightning and on-chain) balances and a summary
    of the opened channels.
    """
    def __init__(self, plugin):
        super(OverviewPage, self).__init__()
        self.setupUi(self)
        self.plugin = plugin
        self.update()

    def update(self):
        """Update the displayed informations from the rpc"""
        funds = self.plugin.rpc.listfunds()
        infos = self.plugin.rpc.getinfo()
        # Condition to prevent for RPC errors
        if infos:
            self.labelAlias.setText(infos["alias"])
            self.labelPublicKey.setText(infos["id"])
            self.labelColor.setText(infos["color"])
            self.labelColor.setStyleSheet("QLabel {background-color: #"+infos["color"]+";}")
            self.labelChannelCountActive.setText(str(infos["num_active_channels"]))
            total_channels = infos["num_active_channels"] + infos["num_inactive_channels"] +\
                    infos["num_pending_channels"]
            self.labelChannelCountTotal.setText(str(total_channels))
            self.labelConnectedNodes.setText(str(infos["num_peers"]))
        # Condition to prevent for RPC errors
        if funds:
            # Note: ln balance is in mbynd but Beyondcoin's one is in mbynd
            ln_balance_av = ln_balance_pen = 0
            for i in funds["channels"]:
                if "short_channel_id" in i:
                    ln_balance_av += int(i["our_amount_mbynd"])
                else:
                    ln_balance_pen += int(i["our_amount_mbynd"])
            self.labelBalanceLightning.setText(str(ln_balance_av) + "MBYND")
            self.labelPendingLightning.setText(str(ln_balance_pen) + "MBYND")
            self.labelLightningTotal.setText(str(ln_balance_av + ln_balance_pen) + "MBYND")
            btc_balance_av = btc_balance_pen = 0
            for i in funds["outputs"]:
                if i["status"] == "confirmed":
                    btc_balance_av += i["value"]
                else:
                    btc_balance_pen += i["value"]
            self.labelBalanceBeyondcoin.setText(str(btc_balance_av) + "BYND")
            self.labelPendingBeyondcoin.setText(str(btc_balance_pen) + "BYND")
            self.labelBeyondcoinTotal.setText(str(btc_balance_av + btc_balance_pen) + "BYND")
