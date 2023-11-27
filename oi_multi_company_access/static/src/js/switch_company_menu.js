/** @odoo-module **/

import { SwitchCompanyMenu, systrayItem } from "@web/webclient/switch_company_menu/switch_company_menu";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";

export class MySwitchCompanyMenu extends SwitchCompanyMenu {
	setup() {
		super.setup(...arguments);
		this.orm = useService("orm");
		this.multi_company_access = session.multi_company_access;

		if (session.multi_company_access && this.selectedCompanies.length > 1) {		
			const router = useService("router");
			const cookie = useService("cookie");
			const nextCompanyIds = [session.company_id];
            router.pushState({ cids: nextCompanyIds }, { lock: true });
            cookie.setCookie("cids", nextCompanyIds);
            browser.setTimeout(() => browser.location.reload()); 
		}
	}

	async logIntoCompany(companyId) {

		if (this.multi_company_access) {
			await this.orm.write("res.users", [session.uid], {
				company_id: companyId,
			});
		}

		super.logIntoCompany(...arguments);
	}
}

systrayItem.Component = MySwitchCompanyMenu;
