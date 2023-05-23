from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.postgres.forms import RangeWidget
from django.contrib.admin.widgets import *
from django.contrib.admin.sites import site


# LOGIN
class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password = forms.CharField(
        widget= forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


# Using User Model
class MasterUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "email", 
            "username",
            "id_mitra", 
            "id_pegawai", 
            "is_mitra",  
            "is_gudang", 
            "is_admin",
            "is_owner", 
            ]
        labels = {
            'is_mitra': ('Role Mitra'),
            'is_gudang': ('Role Gudang'),
            'is_admin': ('Role Admin'),
            'is_owner': ('Role Owner'),
            'id_mitra': ('Kepemilikan Mitra'),
            'id_pegawai': ('Kepemilikan Pegawai'),
        }
class MasterUserSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "email", 
            "username",
            "password1",
            "password2",
            "id_mitra", 
            "id_pegawai", 
            "is_mitra",  
            "is_gudang", 
            "is_admin",
            "is_owner", 
            ]
        labels = {
            'is_mitra': ('Role Mitra'),
            'is_gudang': ('Role Gudang'),
            'is_admin': ('Role Admin'),
            'is_owner': ('Role Owner'),
            'id_mitra': ('Kepemilikan Mitra'),
            'id_pegawai': ('Kepemilikan Pegawai'),
        }


# Using Mitra Model
class MasterMitraForm(forms.ModelForm):
    class Meta:
        model = Mitra
        fields = [
            "nama_mitra", 
            "tgl_lahir", 
            "jenis_kelamin",
            "alamat", 
            "no_hp", 
            "pendidikan",
            "pelatihan",
            "pengalaman_budidaya", 
            "motivasi_bermitra", 
            "periode_kontrak",  
            "id_level_paket",
            "tgl_registrasi", 
            ]
        labels = {
            'nama_mitra': ('Nama Lengkap'),
            'alamat': ('Alamat'),
            'jenis_kelamin': ('Jenis Kelamin'),
            'tgl_lahir': ('Tanggal Lahir'),
            'pendidikan': ('Pendidikan Terakhir'),
            'pelatihan': ('Pelatihan Budidaya yang Pernah Diikuti'),
            'pengalaman_budidaya': ('Pengalaman Budidaya'),
            'motivasi_bermitra': ('Motivasi Bermitra'),
            'periode_kontrak': ('Periode Kontrak (tahun)'),
            'id_level_paket': ('Level Paket'),
            'tgl_registrasi': ('Tanggal Registrasi'),
            'no_hp': ('No HP'),
        }
        widgets = {
            'tgl_lahir': forms.DateInput(attrs={'type': 'date'}),
            'tgl_registrasi': forms.DateInput(attrs={'type': 'date'}),
            'periode_kontrak': forms.NumberInput(attrs={
                'min': '0',
                'placeholder':'tahun'
                }),
            'no_hp': forms.TextInput(attrs={'placeholder': '+628xxxxxxxxxx'}),

        }
class UpdateMitraForm(forms.ModelForm):
    class Meta:
        model = Mitra
        exclude = ('periode_kontrak', 'id_level_paket', 'tgl_registrasi' )
        labels = {
            'nama_mitra': ('Nama Lengkap'),
            'alamat': ('Alamat'),
            'jenis_kelamin': ('Jenis Kelamin'),
            'pendidikan': ('Pendidikan Terakhir'),
            'pelatihan': ('Pelatihan Budidaya yang Pernah Diikuti'),
            'tgl_lahir': ('Tanggal Lahir'),
            'pengalaman_budidaya': ('Pengalaman Budidaya'),
            'motivasi_bermitra': ('Motivasi Bermitra'),
            'no_hp': ('No HP'),
        }

        widgets = {
            'tgl_lahir': forms.DateInput(attrs={'type': 'date'}),
            'no_hp': forms.TextInput(attrs={'placeholder': '+628xxxxxxxxxx'}),

        }


# Using Pegawai Model
class MasterPegawaiForm(forms.ModelForm):
    class Meta:
        model = Pegawai
        fields = '__all__'
        labels = {
            'nama_pegawai': ('Nama Lengkap'),
            'alamat': ('Alamat'),
            'pendidikan': ('Pendidikan Terakhir'),
            'pelatihan': ('Pelatihan Budidaya yang Pernah Diikuti'),
            'tgl_lahir': ('Tanggal Lahir'),
            'pengalaman_kerja': ('Pengalaman Budidaya'),
        }
        widgets = {
            'tgl_lahir': forms.DateInput(attrs={'type': 'date'}),
        }


# Using Level Paket Model
class MasterLevelPaketForm(forms.ModelForm):
    class Meta:
        model = LevelPaket
        fields = '__all__'
        labels = {
            'nama_paket': ('Nama Jenis Paket'),
            'kuota_cacing': ('Kuota Cacing (kg)'),
            'kuota_media_budidaya': ('Kuota Media Budidaya (sak)'),
            'biaya_paket': ('Biaya Paket (Rp)'),
            'kuota_panen': ('Kuota Panen/bln (kg)'),
            'harga_panen': ('Harga Panen/kg (Rp)'),
        }
        widgets = {
            'kuota_cacing': forms.NumberInput(attrs={'placeholder': 'kg'}),
            'kuota_media_budidaya': forms.NumberInput(attrs={'placeholder': 'sak'}),
            'biaya_paket': forms.NumberInput(attrs={'placeholder': 'Rp.'}),
            'kuota_panen': forms.NumberInput(attrs={'placeholder': 'kg'}),
            'harga_panen': forms.NumberInput(attrs={'placeholder': 'Rp.'}),
        }
        
# Using Barang Model
class MasterBarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = '__all__'
        labels = {
            'nama_barang': ('Nama Barang'),
            'stok_gudang': ('Stok Gudang'),
            'satuan': ('Satuan'),
            'deskripsi': ('Deskripsi'),
        }

# Using FAQ Model
class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'


# Using BarangKeluar Model
class BarangKeluarForm(forms.ModelForm):
    class Meta:
        model = BarangKeluar
        fields = '__all__'
        labels = {
            'tgl_keluar_gudang': ('Tanggal Keluar Gudang'),
            'id_barang': ('Nama Barang'),
            'kuantitas_pengambilan': ('Kuantitas Pengambilan'),
            'keterangan': ('Keterangan'),
            'id_mitra': ('Mitra Penerima'),
        }
        widgets = {
            'tgl_keluar_gudang': forms.DateInput(attrs={'type': 'date'}),
        }

class BarangMasukForm(forms.ModelForm):
    class Meta:
        model = BarangMasuk
        fields = '__all__'
        labels = {
            'tgl_masuk_gudang': ('Tanggal Masuk Gudang'),
            'id_barang': ('Nama Barang'),
            'kuantitas_masuk': ('Kuantitas Masuk'),
            'keterangan': ('Keterangan'),
        }
        widgets = {
            'tgl_masuk_gudang': forms.DateInput(attrs={'type': 'date'}),
        }

# Using Notifikasi Model
class GudangReminderFormCreate(forms.ModelForm):
    class Meta:
        model = Notifikasi
        exclude = ('tgl_post', 'status_pelaksanaan')
        labels = {
            'id_mitra': ('Nama Mitra'),
        }
class GudangReminderFormUpdate(forms.ModelForm):
    class Meta:
        model = Notifikasi
        exclude = ('tgl_post', )
        labels = {
            'id_mitra': ('Nama Mitra'),
            'status_pelaksanaan': ('Status'),
        }
class NotifikasiForm(forms.ModelForm):
    class Meta:
        model = Notifikasi
        fields = ['status_pelaksanaan']
        labels = {
            'status_pelaksanaan': ('Status'),
        }


#Using Recording Model
class ProgressBudidayaForm(forms.ModelForm):
    class Meta:
        model = ProgressBudidaya
        fields = '__all__'
        labels = {
            'tgl_pengamatan': ('Tanggal Pengamatan'),
            'lokasi_budidaya': ('Lokasi Budidaya'),
            'id_mitra': ('Nama Mitra'),
            'kondisi_media_budidaya': ('Kondisi Media Budidaya'),
            'perkembangan_cacing': ('Perkembangan Cacing'),
            'keluhan': ('Keluhan'),           
        }
        widgets = {
            'tgl_pengamatan': forms.DateInput(attrs={'type': 'date'}),
        }    
class MitraProgressBudidayaForm(forms.ModelForm):
    class Meta:
        model = ProgressBudidaya
        fields = ['tgl_pengamatan', 'lokasi_budidaya', 'id_mitra', 'kondisi_media_budidaya', 'perkembangan_cacing', 'keluhan']
        labels = {
            'tgl_pengamatan': ('Tanggal Pengamatan'),
            'lokasi_budidaya': ('Lokasi Budidaya'),
            'id_mitra': ('Nama Mitra'),
            'kondisi_media_budidaya': ('Kondisi Media Budidaya'),
            'perkembangan_cacing': ('Perkembangan Cacing'),
            'keluhan': ('Keluhan'),           
        }
        widgets = {
            'tgl_pengamatan': forms.DateInput(attrs={'type': 'date'}),
        }    

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)
        if user_id:
            self.fields['id_mitra'].initial = user_id
            self.fields['id_mitra'].queryset = Mitra.objects.filter(id_mitra=user_id)


# Using Panen Model
class PanenForm(forms.ModelForm):
    class Meta:
        model = Panen
        fields = '__all__'
        labels = {
            'id_mitra': ('Nama Mitra'),
            'tgl_panen': ('Tanggal Panen'),
            'umur_panen': ('Umur Cacing (bulan)'),
            'berat_hasil_panen': ('Berat Bersih Hasil Panen (kg)'),
            'catatan_kelayakan_hasil_panen': ('Catatan Kelayakan Hasil Panen'),

        }
        widgets = {
            'tgl_panen': forms.DateInput(attrs={'type': 'date', 'format': 'YYYY-MM-DD'}),
            'umur_panen': forms.NumberInput(attrs={'placeholder': 'bulan'}),
            'berat_hasil_panen': forms.NumberInput(attrs={'placeholder': 'kg'}),
        }    





# Using Pelatihan Model
class PelatihanForm(forms.ModelForm):
    class Meta:
        model = Pelatihan
        fields = '__all__'
        labels = {
            'status_pendaftaran': ('Status Pendaftaran'),
            'jenis_pelatihan': ('Jenis Pelatihan'),
            'gelombang': ('Gelombang'),
            'kuota': ('Kuota Peserta'),
            'awal_periode_pendaftaran': ('Awal Periode Pendaftaran'),
            'akhir_periode_pendaftaran': ('Akhir Periode Pendaftaran'),
            'awal_periode_pelatihan': ('Awal Periode Pelatihan'),
            'akhir_periode_pelatihan': ('Akhir Periode Pelatihan'),
            'tempat_penyelenggaraan': ('Tempat Penyelenggaraan'),
            'contact_person': ('Contact Person'),
            'link_pendaftaran': ('Link GForm Pendaftaran '),
        }
        
        widgets = {
            'awal_periode_pendaftaran': forms.DateInput(attrs={'type': 'date'}),
            'akhir_periode_pendaftaran': forms.DateInput(attrs={'type': 'date'}),
            'kuota': forms.NumberInput(attrs={'placeholder': 'peserta'}),
            'awal_periode_pelatihan': forms.DateInput(attrs={'type': 'date'}),
            'akhir_periode_pelatihan': forms.DateInput(attrs={'type': 'date'}),
            'link_pendaftaran': forms.URLInput(attrs={'class': 'form-control'})

            # 'periode_pendaftaran': RangeWidget(
            #     attrs={
            #         'type': 'date',
            #         'class': 'form-control',
            #         'placeholder': 'MM/DD/YYYY',
            #     },
            #     base_widget=forms.DateInput(attrs={
            #         'type': 'date',
            #         'class': 'form-control',
            #         'placeholder': 'MM/DD/YYYY',
            #     }),
            # ),

            # 'periode_pelatihan': RangeWidget(
            #     attrs={
            #         'type': 'date',
            #         'class': 'form-control',
            #         'placeholder': 'MM/DD/YYYY',
            #     },
            #     base_widget=forms.DateInput(attrs={
            #         'type': 'date',
            #         'class': 'form-control',
            #         'placeholder': 'MM/DD/YYYY',
            #     }),
            # ),


        }    

