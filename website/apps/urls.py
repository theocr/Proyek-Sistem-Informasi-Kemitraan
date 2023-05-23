from django.urls import path, include
from apps import views
from django.contrib.auth.views import *

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path('mitra/', include([
        path('', views.mitra_notifikasi, name='mitra_dashboard'),
        path('notifikasi/', views.mitra_notifikasi, name='mitra_notifikasi'),
        path('notifikasi/<int:id>', views.mitra_notifikasi_update, name='mitra_notifikasi_update'),
        path('profil/', views.mitra_profil, name='mitra_profil'),
        path('faq/', views.mitra_faq, name='mitra_faq'),
        path('progress-budidaya/', views.mitra_progress_budidaya, name='mitra_progress_budidaya'),
        path('status-keanggotaan/', views.mitra_status_anggota, name='mitra_status-keanggotaan'),
        path('pelatihan/', views.mitra_pelatihan, name='mitra_pelatihan'),
        path('pelatihan/detail/<int:id>/', views.mitra_detail_pelatihan, name='mitra_pelatihan_detail'),

    ])),

    path('administrator/', include([
        path('', views.admin_dashboard, name='admin_dashboard'),
        path('list-mitra/', views.admin_manage_mitra, name='admin_mitra'),
        path('list-mitra/update/raj-mitra-<int:id>/', views.admin_manage_mitra_update, name='admin_mitra_update'),
        path('list-mitra/delete/raj-mitra-<int:id>/', views.admin_manage_mitra_delete, name='admin_mitra_delete'),
        path('list-pegawai/', views.admin_manage_pegawai, name='admin_pegawai'),
        path('list-pegawai/update/<int:id>/', views.admin_manage_pegawai_update, name='admin_pegawai_update'),
        path('list-pegawai/delete/<int:id>/', views.admin_manage_pegawai_delete, name='admin_pegawai_delete'),
        path('list-user/', views.admin_manage_user, name='admin_user'),
        path('list-user/update/<int:id>/', views.admin_manage_user_update, name='admin_user_update'),
        path('list-user/delete/<int:id>/', views.admin_manage_user_delete, name='admin_user_delete'),
        path('level-paket/', views.admin_manage_level_paket, name='admin_level-paket'),
        path('level-paket/update/<int:id>/', views.admin_manage_level_paket_update, name='admin_level-paket_update'),
        path('level-paket/delete/<int:id>/', views.admin_manage_level_paket_delete, name='admin_level-paket_delete'),
    ])),

    path('owner/', include([
        path('', views.owner_dashboard, name='owner_dashboard'),
        path('list-mitra/', views.owner_list_mitra, name='owner_list_mitra'),
        path('target-produksi/', views.owner_laporan_target_produksi, name='owner_target_produksi'),
        path('hasil-panen/', views.owner_laporan_hasil_panen, name='owner_hasil_panen'),
        path('rekap-target-realisasi/', views.owner_rekapitulasi_target_dan_realisasi, name='owner_rekap_target_realisasi'),
        path('detail-mitra/<int:id>/', views.owner_detail_mitra, name='owner_detail_mitra'),
        path('faq/', views.owner_faq, name='owner_faq'),
        path('faq/update/<int:id>/', views.owner_faq_update, name='owner_faq_update'),
        path('faq/delete/<int:id>/', views.owner_faq_delete, name='owner_faq_delete'),
        path('pelatihan/', views.owner_pelatihan, name='owner_pelatihan'),
        path('pelatihan/update/<int:id>/', views.owner_pelatihan_update, name='owner_pelatihan_update'),
        path('pelatihan/delete/<int:id>/', views.owner_pelatihan_delete, name='owner_pelatihan_delete'),
        path('progress-budidaya/', views.owner_record_progress_budidaya, name='owner_record_progress_budidaya'),

    ])),

    path('gudang/', include([
        path('', views.gudang_dashboard, name='gudang_dashboard'),

        path('master-barang/', views.gudang_manage_master_barang, name='gudang-master_barang'),
        path('master-barang/update/<int:id>/', views.gudang_manage_master_barang_update, name='gudang-master_barang_update'),
        path('master-barang/delete/<int:id>/', views.gudang_manage_master_barang_delete, name='gudang-master_barang_delete'),

        path('barang-masuk/', views.gudang_barang_masuk, name='gudang-barang_masuk'),
        path('barang-masuk/update/<int:id>/', views.gudang_barang_masuk_update, name='gudang-barang_masuk_update'),
        path('barang-masuk/delete/<int:id>/', views.gudang_barang_masuk_delete, name='gudang-barang_masuk_delete'),

        path('barang-keluar/', views.gudang_barang_keluar, name='gudang-barang_keluar'),
        path('barang-keluar/update/<int:id>/', views.gudang_barang_keluar_update, name='gudang-barang_keluar_update'),
        path('barang-keluar/delete/<int:id>/', views.gudang_barang_keluar_delete, name='gudang-barang_keluar_delete'),

        path('pesan/', views.gudang_reminder, name='gudang-reminder'),
        path('pesan/detail/<int:id>/', views.gudang_reminder_update, name='gudang-reminder_update'),
        path('pesan/delete/<int:id>/', views.gudang_reminder_delete, name='gudang-reminder_delete'),

        path('progress-budidaya/', views.gudang_progress_budidaya, name='gudang-progress_budidaya'),
        path('progress-budidaya/update/<int:id>/', views.gudang_progress_budidaya_update, name='gudang-progress_budidaya_update'),
        path('progress-budidaya/delete/<int:id>/', views.gudang_progress_budidaya_delete, name='gudang-progress_budidaya_delete'),

        path('panen/', views.gudang_panen, name='gudang-panen'),
        path('panen/update/<int:id>/', views.gudang_panen_update, name='gudang-panen_update'),
        path('panen/delete/<int:id>/', views.gudang_panen_delete, name='gudang-panen_delete'),

        path('detail-mitra/<int:id>/', views.gudang_detail_mitra, name='gudang-detail_mitra'),
        path('list-mitra/', views.gudang_list_mitra, name='gudang-list_mitra'),
    ])),    
]