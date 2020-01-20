# -*- coding: utf-8 -*-
# © 2009 NetAndCo (<http://www.netandco.net>).
# © 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# © 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2018 Daniel Campos <danielcampos@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, tools, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError



class account_journal(models.Model):
    _name = 'account.journal'
    _inherit = 'account.journal'
    
    allow_unbalanced = fields.Boolean(string="Allow unbalanced moves", default=False)


class account_move(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    @api.multi
    def assert_balanced(self):
    
        if self.journal_id.allow_unbalanced == True:
            return True
    
        if not self.ids:
            return True
        self._cr.execute("""\
            SELECT      move_id
            FROM        account_move_line
            WHERE       move_id in %s
            GROUP BY    move_id
            HAVING      abs(sum(debit) - sum(credit)) > 0.00001
            """, (tuple(self.ids),))
        if len(self._cr.fetchall()) != 0:
            raise UserError(_("Cannot create unbalanced journal entry."))
        return True

