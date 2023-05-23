from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from tinymce.models import HTMLField
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import DateRangeField
from datetime import datetime    
import re
from django.core.exceptions import ValidationError


"""
DESKRIPSI:
    Code Model dibawah untuk Customize Multiple User Roles
"""
class CustomUser(AbstractUser):
    is_mitra= models.BooleanField('Role Mitra', default=False)
    is_admin = models.BooleanField('Role Admin', default=False)
    is_gudang = models.BooleanField('Role Gudang', default=False)
    is_owner = models.BooleanField('Role Owner', default=False)

    id_mitra = models.ForeignKey('Mitra', blank=True, null=True, on_delete=models.CASCADE)
    id_pegawai = models.ForeignKey('Pegawai', blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + " " + str(self.id_mitra) + " " + str(self.id_pegawai)


"""
DESKRIPSI:
    Code Model dibawah untuk Membuat Basis Data Business Model Project ini
"""

class Mitra(models.Model):
    class JenisKelamin(models.TextChoices): 
        PR = 'Pria', 'Pria'
        WN = 'Wanita', 'Wanita'
        TM = '-', '-'

    class Pendidikan(models.TextChoices): 
        SD = 'SD', 'SD'
        SMP = 'SMP', 'SMP'
        SMA = 'SMA', 'SMA'
        S1 = 'Sarjana S1', 'Sarjana S1'
    id_mitra = models.BigAutoField(primary_key=True)
    nama_mitra = models.CharField(max_length=50)
    tgl_lahir = models.DateField(auto_now_add=False)
    jenis_kelamin = models.CharField(
        max_length=20,
        choices=JenisKelamin.choices,
        default=JenisKelamin.TM
    )
    alamat = models.TextField()
    no_hp = models.CharField(max_length=20)
    pendidikan = models.CharField(
        max_length=20,
        choices=Pendidikan.choices,
        default=Pendidikan.SMA
    )
    pelatihan = HTMLField()
    pengalaman_budidaya = HTMLField()
    motivasi_bermitra = HTMLField()
    periode_kontrak = models.IntegerField()
    id_level_paket = models.ForeignKey('LevelPaket', null=True, on_delete=models.SET_NULL)
    tgl_registrasi = models.DateField(default=datetime.now)
    def clean(self):
        """
        DESKRIPSI:
            Input ini dimulai dengan kode negara +62 untuk Indonesia, 
            diikuti dengan nomor ponsel yang valid dengan kode negara yang dihapus. 
            Nomor harus dimulai dengan 8 dan memiliki antara 9 dan 14 digit (termasuk 8 di depan). 
            Regex akan mencocokkan input ini dan menyimpannya di kolom whatsapp_number dengan 
            menambahkan kode negara +62
        """

        # Regular expression to match WhatsApp numbers
        no_hp_regex = r'^\+?(?:62|\(62\)|0)?([8][1-9]\d{7,12})$'

        # Validate the WhatsApp number using the regular expression
        match = re.match(no_hp_regex, self.no_hp)
        if not match:
            raise ValidationError("Nomor HP Tidak Valid")
        self.no_hp = f"+62{match.group(1)}"

    def __str__(self):
        return  "RAJ-MITRA-" + str(self.id_mitra) + " | " + str(self.nama_mitra) 

class Pegawai(models.Model):
    id_pegawai = models.BigAutoField(primary_key=True)
    class Pendidikan(models.TextChoices): 
        SD = 'SD', 'SD'
        SMP = 'SMP', 'SMP'
        SMA = 'SMA', 'SMA'
        S1 = 'S1', 'Sarjana S1'
    nama_pegawai = models.CharField(max_length=50)
    tgl_lahir = models.DateField()
    alamat = models.TextField()
    pendidikan = models.CharField(
        max_length=20,
        choices=Pendidikan.choices,
        default=Pendidikan.SMA
    )
    pelatihan = HTMLField()
    pengalaman_kerja = HTMLField()

    def __str__(self):
        return "RAJ-KARY-" + str(self.id_pegawai)

class LevelPaket(models.Model):
    id_level_paket = models.BigAutoField(primary_key=True) 
    nama_paket = models.CharField(max_length=7)
    kuota_cacing = models.IntegerField()
    kuota_media_budidaya = models.IntegerField()                    
    biaya_paket = models.IntegerField()
    kuota_panen = models.IntegerField()
    harga_panen = models.IntegerField()

    def __str__(self):
        return self.nama_paket

class Panen(models.Model):
    id_panen = models.BigAutoField(primary_key=True)
    id_mitra = models.ForeignKey('Mitra', null=True, on_delete=models.SET_NULL)
    tgl_panen = models.DateField(default=datetime.now)
    berat_hasil_panen = models.IntegerField()
    catatan_kelayakan_hasil_panen = HTMLField()

class ProgressBudidaya(models.Model):
    id_progress_budidaya = models.BigAutoField(primary_key=True)
    tgl_pengamatan = models.DateField(default=datetime.now)
    lokasi_budidaya = models.CharField(max_length=100)
    id_mitra = models.ForeignKey('Mitra', null=True, on_delete=models.SET_NULL)
    kondisi_media_budidaya = HTMLField()
    perkembangan_cacing = HTMLField()
    keluhan = HTMLField()
    class PenilaianGudang(models.TextChoices): 
        aman = 'TERKONTROL', 'TERKONTROL'
        danger = 'PERLU PENGAWASAN', 'PERLU PENGAWASAN'
    penilaian_gudang = models.CharField(
       max_length=20,
       choices=PenilaianGudang.choices,
       default=PenilaianGudang.danger,
    )

class FAQ(models.Model):
    id_faq = models.BigAutoField(primary_key=True)
    pertanyaan = HTMLField()
    jawaban = HTMLField()

    def __str__(self):
        return "FAQ-" + str(self.id_faq)

class Notifikasi(models.Model):
    id_notifikasi = models.BigAutoField(primary_key=True)
    judul = HTMLField()
    pesan = HTMLField()
    id_mitra = models.ForeignKey('Mitra', null=True, on_delete=models.SET_NULL) #kalau pada saat tambah data bisa dikosongan, tambahkan blank=True, bisa ditaruh sebelum null
    tgl_post = models.DateField(default=datetime.now)
    class Status(models.TextChoices): 
        done = 'DONE', 'DONE'
        progress = 'PROGRESS', 'PROGRESS'
    status_pelaksanaan = models.CharField(
       max_length=20,
       choices=Status.choices,
       default=Status.progress
    )

class Barang(models.Model):
    id_barang = models.BigAutoField(primary_key=True)
    nama_barang = models.CharField(max_length=50)
    stok_gudang = models.IntegerField()
    satuan = models.CharField(max_length=10)
    deskripsi = models.TextField()

    def __str__(self):
        return str(self.nama_barang)
 
class BarangKeluar(models.Model):
    id_barang_keluar = models.BigAutoField(primary_key=True)
    id_barang = models.ForeignKey('Barang', null=True, on_delete=models.SET_NULL) 
    id_mitra = models.ForeignKey('Mitra', blank=True, null=True, on_delete=models.CASCADE)
    tgl_keluar_gudang = models.DateField(default=datetime.now)
    kuantitas_pengambilan = models.IntegerField()
    keterangan = models.TextField()

@receiver(post_save, sender=BarangKeluar)
def decrease_stok_barang(sender, instance, created, **kwargs):
    instance.id_barang.stok_gudang -= instance.kuantitas_pengambilan
    instance.id_barang.save()

class BarangMasuk(models.Model):
    id_barang_masuk = models.BigAutoField(primary_key=True)
    id_barang = models.ForeignKey('Barang', null=True, on_delete=models.SET_NULL) 
    tgl_masuk_gudang = models.DateField(default=datetime.now)
    kuantitas_masuk = models.IntegerField()
    keterangan = models.TextField()

@receiver(post_save, sender=BarangMasuk)
def increase_stok_barang(sender, instance, created, **kwargs):
    instance.id_barang.stok_gudang += instance.kuantitas_masuk
    instance.id_barang.save()














class Pelatihan(models.Model):
    id_pelatihan = models.BigAutoField(primary_key=True)
    class StatusPendaftaran(models.TextChoices): 
        buka = 'TUTUP', 'TUTUP'
        tutup = 'AKTIF', 'AKTIF'
        belum_aktif = 'BELUM AKTIF', 'BELUM AKTIF'
    status_pendaftaran = models.CharField(
       max_length=20,
       choices=StatusPendaftaran.choices,
       default=StatusPendaftaran.belum_aktif
    )
    jenis_pelatihan = models.TextField()
    nama_pelatihan = models.TextField()
    gelombang = models.TextField()
    kuota = models.IntegerField()
    awal_periode_pendaftaran = models.DateField()
    akhir_periode_pendaftaran = models.DateField()

    awal_periode_pelatihan = models.DateField()
    akhir_periode_pelatihan = models.DateField()

    tempat_penyelenggaraan = models.TextField()
    contact_person = models.TextField()
    link_pendaftaran = models.URLField(max_length=200)