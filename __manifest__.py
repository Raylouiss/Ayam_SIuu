# -*- coding: utf-8 -*-
{
    'name': "Aplikasi Pemantauan dan Pencatatan Gudang",
    'summary': 'Module Odoo untuk mengelola pergudangan',
    'description': 'Module Odoo untuk membantu perusahaan dalam mencatat inventaris harian, memantau penyimpanan bahan baku, dan evaluasi terhadap pengolahan bahan produksi.',
    'sequence': -100,
    'author': "Ayam SIuu",
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/inventory_menus.xml',
        'views/inventory_trees.xml',
        'views/inventory_forms.xml',
    ],
    'demo': [
        
    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
