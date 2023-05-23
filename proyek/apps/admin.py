from django.contrib import admin
from .models import *

# Register your models here.
models = [Pelatihan, CustomUser, Notifikasi, Mitra, LevelPaket, Barang, BarangKeluar, BarangMasuk, Pegawai, Panen, ProgressBudidaya, FAQ]

for model in models:
    admin.site.register(model)

