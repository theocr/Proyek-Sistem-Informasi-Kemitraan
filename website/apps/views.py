from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models.functions import *
from django.db.models import *
from django.utils import timezone
from django.db import models
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from .decorators import *


def home(request):
    return redirect('login')

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                # request.session['user_id'] = user.id_pegawai.id_pegawai
                # user_id = user.id_pegawai.id_pegawai
                return redirect('admin_dashboard')
            elif user is not None and user.is_owner:
                login(request, user)
                # request.session['user_id'] = user.id_pegawai.id_pegawai
                # user_id = user.id_pegawai.id_pegawai
                return redirect('owner_dashboard')
            elif user is not None and user.is_gudang:
                login(request, user)
                # request.session['user_id'] = user.id_pegawai.id_pegawai
                # user_id = user.id_mitra.id_mitra
                return redirect('gudang_dashboard')
            elif user is not None and user.is_mitra:
                login(request, user)
                request.session['user_id'] = user.id_mitra.id_mitra
                user_id = user.id_mitra.id_mitra
                return redirect('mitra_dashboard')
            else:
                msg = '*username dan password masih salah atau akun belum terdaftar'
        else:
            msg = 'Error validating the form'
    return render(request, "accounts/login.html", {
        "form": form, 
        "msg": msg
    })

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('login')



"""
DESKRIPSI:
    View ini hanya dapat diakses oleh Role Mitra
"""
@mitra_required 
def mitra_notifikasi(request):
    user_id = request.session.get('user_id') 
    mitra_model = get_object_or_404(Mitra, id_mitra=user_id)

    if user_id is not None:
        notifikasi_query = Notifikasi.objects.select_related('id_mitra').all()
        notifikasi_query = notifikasi_query.filter(id_mitra=user_id)
        notifikasi_data = notifikasi_query.count()

        return render(request, 'menu/mitra/mitra-notifikasi.html', {
            "notifikasi_query": notifikasi_query,
            'notifikasi_data':notifikasi_data,
            'mitra_model':mitra_model
            }
            )
    else:
        return redirect('login')

# Memang seperti ini adanya kalo notifikasi dengan id auto increment rawan diketahui, makanya ada namanya UUID untuk membuat idnya sulit ditebak
@mitra_required
def mitra_notifikasi_update(request, id):
    user_id = request.session.get('user_id')
    mitra_model = get_object_or_404(Mitra, id_mitra=user_id)

    if user_id is not None:
        notifikasi_query = Notifikasi.objects.select_related('id_mitra').all()
        notifikasi_query = notifikasi_query.filter(id_mitra=user_id)
        notifikasi_data = notifikasi_query.count()

        notifikasi_model = get_object_or_404(Notifikasi, id_notifikasi=id)
        form = NotifikasiForm(request.POST or None, instance=notifikasi_model)
        if form.is_valid():
            form.save()
            return redirect('mitra_notifikasi')
        
        return render(request, 'menu/mitra/mitra-notifikasi_update.html', {
            "notifikasi_model":notifikasi_model,    
            "form": form,
            "notifikasi_data": notifikasi_data,
            "mitra_model":mitra_model
            })
    else:
        return redirect('login')

@mitra_required 
def mitra_profil(request):
    user_id = request.session.get('user_id') 
    if user_id is not None:
        notifikasi_query = Notifikasi.objects.select_related('id_mitra').all()
        notifikasi_query = notifikasi_query.filter(id_mitra=user_id)
        notifikasi_data = notifikasi_query.count()

        mitra_model = get_object_or_404(Mitra, id_mitra=user_id)
        form = UpdateMitraForm(request.POST or None, instance=mitra_model)
        if form.is_valid():
            form.save()
            return redirect('mitra_profil')            
        return render(request, 'menu/mitra/mitra-profil.html', {
            'form': form,
            'mitra_model':mitra_model,
            'notifikasi_data':notifikasi_data}
            )
    else:
        return redirect('login')

@mitra_required 
def mitra_progress_budidaya(request):
    user_id = request.session.get('user_id') 
    mitra_model = get_object_or_404(Mitra, id_mitra=user_id)

    if user_id is not None:
        notifikasi_query = Notifikasi.objects.select_related('id_mitra').all()
        notifikasi_query = notifikasi_query.filter(id_mitra=user_id)
        notifikasi_data = notifikasi_query.count()

        if request.method == 'POST':
            form = MitraProgressBudidayaForm(request.POST, user_id=user_id)
            if form.is_valid():
                form.save()
                return redirect('mitra_progress_budidaya')            
        else:
            form = MitraProgressBudidayaForm(user_id=user_id)
            
        return render(request, 'menu/mitra/mitra-progress_budidaya.html', {
            'form': form,
            'notifikasi_data': notifikasi_data,
            'mitra_model': mitra_model,

            })
    else:
        return redirect('login')

@mitra_required 
def mitra_status_anggota(request):
    user_id = request.session.get('user_id') 

    if user_id is not None:
        mitra_data = Mitra.objects.get(id_mitra=user_id)
        notifikasi_query = Notifikasi.objects.select_related('id_mitra').all()
        notifikasi_query = notifikasi_query.filter(id_mitra=user_id)
        notifikasi_data = notifikasi_query.count()

        mitra_model = get_object_or_404(Mitra, id_mitra=user_id)

        try:
            barang_keluar_model = BarangKeluar.objects.get(id_mitra=user_id)
        except BarangKeluar.DoesNotExist:
            barang_keluar_model = None

        return render(request, 'menu/mitra/mitra-status_anggota.html', {
            'mitra_data':mitra_data,
            'mitra_model':mitra_model,
            'barang_keluar_model':barang_keluar_model,
            'notifikasi_data':notifikasi_data}
            )
    else:
        return redirect('login')

@mitra_required
def mitra_faq(request):
    user_id = request.session.get('user_id')
    mitra_model = get_object_or_404(Mitra, id_mitra=user_id)
 
    if user_id is not None:
        notifikasi_query = Notifikasi.objects.select_related('id_mitra').all()
        notifikasi_query = notifikasi_query.filter(id_mitra=user_id)
        notifikasi_data = notifikasi_query.count()

        faq_models = FAQ.objects.all()
        return render(request, "menu/mitra/mitra-faq.html", {
            'faq_models': faq_models, 
            'notifikasi_data':notifikasi_data, 
            'mitra_model':mitra_model}
            )
    else:
        return redirect('login')


@mitra_required
def mitra_pelatihan(request):
    user_id = request.session.get('user_id')
    mitra_model = get_object_or_404(Mitra, id_mitra=user_id)
 
    if user_id is not None:
        notifikasi_query = Notifikasi.objects.select_related('id_mitra').all()
        notifikasi_query = notifikasi_query.filter(id_mitra=user_id)
        notifikasi_data = notifikasi_query.count()

        pelatihan_model = Pelatihan.objects.all()
        return render(request, 'menu/mitra/mitra-pelatihan.html', {
            "pelatihan_model": pelatihan_model,
            'notifikasi_data':notifikasi_data, 
            'mitra_model':mitra_model}
            )

    else:
        return redirect('login')


@mitra_required
def mitra_detail_pelatihan(request, id):
    user_id = request.session.get('user_id')
    mitra_model = get_object_or_404(Mitra, id_mitra=user_id)
 
    if user_id is not None:
        notifikasi_query = Notifikasi.objects.select_related('id_mitra').all()
        notifikasi_query = notifikasi_query.filter(id_mitra=user_id)
        notifikasi_data = notifikasi_query.count()

        pelatihan_data = Pelatihan.objects.get(id_pelatihan=id)
        pelatihan_model = get_object_or_404(Pelatihan, id_pelatihan=id)

        pelatihan_detail = Pelatihan.objects.all().filter(id_pelatihan=id)
        if pelatihan_detail.exists():
            pelatihan_jenis = pelatihan_detail.first().jenis_pelatihan
            pelatihan_nama = pelatihan_detail.first().nama_pelatihan
            pelatihan_gelombang = pelatihan_detail.first().gelombang

            pelatihan_awal_daftar = pelatihan_detail.first().awal_periode_pendaftaran

            pelatihan_akhir_daftar = pelatihan_detail.first().akhir_periode_pendaftaran

            pelatihan_awal_mulai = pelatihan_detail.first().awal_periode_pelatihan

            pelatihan_akhir_mulai = pelatihan_detail.first().akhir_periode_pelatihan

            pelatihan_kuota = pelatihan_detail.first().kuota
            pelatihan_cp = pelatihan_detail.first().contact_person
            pelatihan_link_daftar = pelatihan_detail.first().link_pendaftaran

        else:
            pelatihan_detail = ""



        return render(request, 'menu/mitra/mitra-pelatihan_detail.html', {
            "pelatihan_model": pelatihan_model,
            'notifikasi_data':notifikasi_data, 
            'mitra_model':mitra_model,
            "pelatihan_jenis": pelatihan_jenis,
            "pelatihan_nama": pelatihan_nama,
            "pelatihan_awal_daftar": pelatihan_awal_daftar,
            "pelatihan_akhir_daftar": pelatihan_akhir_daftar,
            "pelatihan_gelombang": pelatihan_gelombang,
            "pelatihan_awal_mulai": pelatihan_awal_mulai,
            "pelatihan_akhir_mulai": pelatihan_akhir_mulai,
            "pelatihan_kuota": pelatihan_kuota,
            "pelatihan_cp": pelatihan_cp,
            "pelatihan_link_daftar": pelatihan_link_daftar,

            
            })
            

    else:
        return redirect('login')


"""
DESKRIPSI:
    View ini hanya dapat diakses oleh Role Admin
"""
@admin_required
def admin_dashboard(request):
    return redirect('admin_mitra')

@admin_required
def admin_manage_mitra(request):
    if request.method == 'POST':
        form = MasterMitraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_mitra')            
    else:
        form = MasterMitraForm()

    mitra_query = Mitra.objects.all()
    return render(request, 'menu/admin/admin-master_mitra.html', {
        "mitra_query": mitra_query,
        'form': form}
        )

@admin_required
def admin_manage_mitra_update(request, id):
    mitra_data = Mitra.objects.get(id_mitra=id)
    mitra_model = get_object_or_404(Mitra, id_mitra=id)
    form = MasterMitraForm(request.POST or None, instance=mitra_model)
    if form.is_valid():
        form.save()
        return redirect('admin_mitra')
    return render(request, 'menu/admin/admin-master_mitra_update.html', {
        "mitra_model":mitra_model, 
        "form": form,
        "mitra_data": mitra_data,
        })

@admin_required
def admin_manage_mitra_delete(request, id):
    mitra_data = Mitra.objects.get(id_mitra=id)
    mitra_data.delete()
    return redirect('admin_mitra')

@admin_required
def admin_manage_pegawai(request):
    if request.method == 'POST':
        form = MasterPegawaiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_pegawai')            
    else:
        form = MasterPegawaiForm()

    pegawai_query = Pegawai.objects.annotate(id_baru=Concat(Value('RAJ-KARY-'), Cast('id_pegawai', CharField())))
    return render(request, 'menu/admin/admin-master_pegawai.html', {
        "pegawai_query": pegawai_query,
        'form': form}
        )

@admin_required
def admin_manage_pegawai_update(request, id):
    pegawai_data = Pegawai.objects.get(id_pegawai=id)
    pegawai_model = get_object_or_404(Pegawai, id_pegawai=id)
    form = MasterPegawaiForm(request.POST or None, instance=pegawai_model)
    if form.is_valid():
        form.save()
        return redirect('admin_pegawai')
    return render(request, 'menu/admin/admin-master_pegawai_update.html', {
        "pegawai_model":pegawai_model, 
        "form": form,
        "pegawai_data": pegawai_data,
        })

@admin_required
def admin_manage_pegawai_delete(request, id):
    pegawai_data = Pegawai.objects.get(id_pegawai=id)
    pegawai_data.delete()
    return redirect('admin_pegawai')

# Hanya admin yang bisa nambah akun baru, melalui view ini. 
@admin_required
def admin_manage_user(request):
    if request.method == 'POST':
        form = MasterUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_user')            
    else:
        form = MasterUserSignUpForm()

    user_query = CustomUser.objects.all()
    return render(request, 'menu/admin/admin-master_user.html', {
        "user_query": user_query,
        'form': form}
        )

@admin_required
def admin_manage_user_update(request, id):
    user_data = CustomUser.objects.get(id=id)
    user_model = get_object_or_404(CustomUser, id=id)
    form = MasterUserForm(request.POST or None, instance=user_model)
    if form.is_valid():
        form.save()
        return redirect('admin_user')
    return render(request, 'menu/admin/admin-master_user_update.html', {
        "user_model":user_model, 
        "form": form,
        "user_data": user_data,
        })

@admin_required
def admin_manage_user_delete(request, id):
    user_data = CustomUser.objects.get(id=id)
    user_data.delete()
    return redirect('admin_user')

@admin_required
def admin_manage_level_paket(request):
    if request.method == 'POST':
        form = MasterLevelPaketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_level-paket')
    else:
        form = MasterLevelPaketForm()

    level_paket_query = LevelPaket.objects.all()
    return render(request, 'menu/admin/admin-master_level_paket.html', {
        "level_paket_query": level_paket_query,
        'form': form}
        )

@admin_required
def admin_manage_level_paket_update(request, id):
    level_paket_data = LevelPaket.objects.get(id_level_paket=id)
    level_paket_model = get_object_or_404(LevelPaket, id_level_paket=id)
    form = MasterLevelPaketForm(request.POST or None, instance=level_paket_model)
    if form.is_valid():
        form.save()
        return redirect('admin_level-paket')
    return render(request, 'menu/admin/admin-master_level_paket_update.html', {
        "level_paket_model":level_paket_model, 
        "form": form,
        "level_paket_data": level_paket_data,
        })

@admin_required
def admin_manage_level_paket_delete(request, id):
        level_paket_data = LevelPaket.objects.get(id_level_paket=id)
        level_paket_data.delete()
        return redirect('admin_level-paket')



"""
DESKRIPSI:
    View ini hanya dapat diakses oleh Role Gudang
"""
@gudang_required
def gudang_dashboard(request):
    return redirect('gudang-master_barang')

@gudang_required
def gudang_manage_master_barang(request):
    if request.method == 'POST':
        form = MasterBarangForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gudang-master_barang')
    else:
        form = MasterBarangForm()

    barang_query = Barang.objects.annotate(id_baru=Concat(Value('BAR-'), Cast('id_barang', CharField())))
    return render(request, 'menu/gudang/gudang-master_barang.html', {
        "barang_query": barang_query,
        'form': form}
        )

@gudang_required
def gudang_manage_master_barang_update(request, id):
    barang_data = Barang.objects.get(id_barang=id)
    barang_model = get_object_or_404(Barang, id_barang=id)
    form = MasterBarangForm(request.POST or None, instance=barang_model)
    if form.is_valid():
        form.save()
        return redirect('gudang-master_barang')
    return render(request, 'menu/gudang/gudang-master_barang_update.html', {
        "barang_model":barang_model, 
        "form": form,
        "barang_data": barang_data,
        })

@gudang_required
def gudang_manage_master_barang_delete(request, id):
        barang_data = Barang.objects.get(id_barang=id)
        barang_data.delete()
        messages.success(request, 'Berhasil Hapus Data Master Barang')
        return redirect('gudang-master_barang')

@gudang_required
def gudang_barang_keluar(request):
    if request.method == 'POST':
        form = BarangKeluarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gudang-barang_keluar')            
    else:
        form = BarangKeluarForm()
    barang_keluar = BarangKeluar.objects.select_related('id_barang').all()


    return render(request, 'menu/gudang/gudang-barang_keluar.html', {
        "barang_keluar": barang_keluar,
        'form': form}
        )

@gudang_required
def gudang_barang_keluar_update(request, id):
    barang_keluar_data = BarangKeluar.objects.get(id_barang_keluar=id)
    barang_keluar_model = get_object_or_404(BarangKeluar, id_barang_keluar=id)
    form = BarangKeluarForm(request.POST or None, instance=barang_keluar_model)
    if form.is_valid():
        form.save()
        return redirect('gudang-barang_keluar')
    return render(request, 'menu/gudang/gudang-barang_keluar_update.html', {
        "barang_keluar_model":barang_keluar_model,    
        "form": form,
        "barang_keluar_data": barang_keluar_data,
        })

@gudang_required
def gudang_barang_keluar_delete(request, id):
    barang_keluar_data = BarangKeluar.objects.get(id_barang_keluar=id)
    barang_keluar_data.delete()
    return redirect('gudang-barang_keluar')

@gudang_required
def gudang_barang_masuk(request):
    if request.method == 'POST':
        form = BarangMasukForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gudang-barang_masuk')            
    else:
        form = BarangMasukForm()
    barang_masuk = BarangMasuk.objects.select_related('id_barang').all()


    return render(request, 'menu/gudang/gudang-barang_masuk.html', {
        "barang_masuk": barang_masuk,
        'form': form}
        )

@gudang_required
def gudang_barang_masuk_update(request, id):
    barang_masuk_data = BarangMasuk.objects.get(id_barang_masuk=id)
    barang_masuk_model = get_object_or_404(BarangMasuk, id_barang_masuk=id)
    form = BarangMasukForm(request.POST or None, instance=barang_masuk_model)
    if form.is_valid():
        form.save()
        return redirect('gudang-barang_masuk')
    return render(request, 'menu/gudang/gudang-barang_masuk_update.html', {
        "barang_masuk_model":barang_masuk_model,    
        "form": form,
        "barang_masuk_data": barang_masuk_data,
        })

@gudang_required
def gudang_barang_masuk_delete(request, id):
    barang_masuk_data = BarangMasuk.objects.get(id_barang_masuk=id)
    barang_masuk_data.delete()
    return redirect('gudang-barang_masuk')

@gudang_required
def gudang_reminder(request):
    if request.method == 'POST':
        form = GudangReminderFormCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gudang-reminder')            
    else:
        form = GudangReminderFormCreate()

    reminder_query = Notifikasi.objects.select_related('id_mitra').all()
    reminder_query = reminder_query.select_related('id_mitra__id_level_paket').all()

    return render(request, 'menu/gudang/gudang-reminder.html', {
        "reminder_query": reminder_query,
        'form': form}
        )

@gudang_required
def gudang_reminder_update(request, id):
    reminder_data = Notifikasi.objects.get(id_notifikasi=id)
    reminder_model = get_object_or_404(Notifikasi, id_notifikasi=id)
    form = GudangReminderFormUpdate(request.POST or None, instance=reminder_model)
    if form.is_valid():
        form.save()
        return redirect('gudang-reminder')
    return render(request, 'menu/gudang/gudang-reminder_update.html', {
        "reminder_model":reminder_model,    
        "form": form,
        "reminder_data": reminder_data,
        })

@gudang_required
def gudang_reminder_delete(request, id):
    reminder_data = Notifikasi.objects.get(id_notifikasi=id)
    reminder_data.delete()
    return redirect('gudang-reminder')

@gudang_required
def gudang_manage_level_paket(request):
    if request.method == 'POST':
        form = MasterLevelPaketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gudang_level-paket')         
    else:
        form = MasterLevelPaketForm()

    level_paket_query = LevelPaket.objects.all()
    return render(request, 'menu/gudang/gudang-master_level_paket.html', {
        "level_paket_query": level_paket_query,
        'form': form}
        )

@gudang_required
def gudang_manage_level_paket_update(request, id):
    level_paket_data = LevelPaket.objects.get(id=id)
    level_paket_model = get_object_or_404(LevelPaket, id=id)
    form = MasterLevelPaketForm(request.POST or None, instance=level_paket_model)
    if form.is_valid():
        form.save()
        return redirect('gudang-master_level_paket')
    return render(request, 'menu/gudang/gudang-master_level_paket_update.html', {
        "level_paket_model":level_paket_model, 
        "form": form,
        "level_paket_data": level_paket_data,
        })

@gudang_required
def gudang_manage_level_paket_delete(request, id):
        level_paket_data = LevelPaket.objects.get(id=id)
        level_paket_data.delete()
        return redirect('gudang_level-paket')

@gudang_required
def gudang_progress_budidaya(request):
    progress_budidaya = ProgressBudidaya.objects.select_related('id_mitra').all()
    # progress_budidaya = progress_budidaya.annotate(
    #     id_baru=Concat(Value('RAJ-MITRA-'), Cast('id_mitra', CharField())),
    #     current_date=Now(),
    #     umur=ExpressionWrapper(
    #         timezone.now().date() - F('id_mitra__tgl_registrasi'),
    #         output_field=models.DurationField()
    #     )
    # )  

    if request.method == 'POST':
        form_progress_budidaya = ProgressBudidayaForm(request.POST)
        if form_progress_budidaya.is_valid():
            form_progress_budidaya.save()
            return redirect('gudang-progress_budidaya')         
    else:
        form_progress_budidaya = ProgressBudidayaForm()


    return render(request, 'menu/gudang/gudang-progress_budidaya.html', {
        "progress_budidaya":progress_budidaya, 
        "form_progress_budidaya":form_progress_budidaya
        })

@gudang_required
def gudang_progress_budidaya_update(request, id):
    progress_budidaya_data = ProgressBudidaya.objects.get(id_progress_budidaya=id)
    progress_budidaya_model = get_object_or_404(ProgressBudidaya, id_progress_budidaya=id)
    form = ProgressBudidayaForm(request.POST or None, instance=progress_budidaya_model)
    if form.is_valid():
        form.save()
        return redirect('gudang-progress_budidaya')
    return render(request, 'menu/gudang/gudang-progress_budidaya_update.html', {
        "progress_budidaya_model":progress_budidaya_model, 
        "form": form,
        "progress_budidaya_data": progress_budidaya_data,
        })

@gudang_required
def gudang_progress_budidaya_delete(request, id):
        progress_budidaya_data = ProgressBudidaya.objects.get(id_progress_budidaya=id)
        progress_budidaya_data.delete()
        return redirect('gudang-progress_budidaya')

@gudang_required
def gudang_panen(request):
    panen = Panen.objects.select_related('id_mitra').all()
    panen = panen.select_related('id_mitra__id_level_paket').all()

    # panen = panen.annotate(
    #     id_baru=Concat(Value('MIT-'), Cast('id_mitra', CharField())),
    #     current_date=Now(),
    # )  

    if request.method == 'POST':
        form_panen = PanenForm(request.POST)
        if form_panen.is_valid():
            form_panen.save()
            return redirect('gudang-panen')         
    else:
        form_panen = PanenForm()


    return render(request, 'menu/gudang/gudang-panen.html', {
        "panen":panen, 
        "form_panen":form_panen
        })

@gudang_required
def gudang_panen_update(request, id):
    panen_data = Panen.objects.get(id_panen=id)
    panen_model = get_object_or_404(Panen, id_panen=id)
    form = PanenForm(request.POST or None, instance=panen_model)
    if form.is_valid():
        form.save()
        return redirect('gudang-panen')
    return render(request, 'menu/gudang/gudang-panen_update.html', {
        "panen_model":panen_model, 
        "form": form,
        "panen_data": panen_data,
        })

@gudang_required
def gudang_panen_delete(request, id):
        panen_data = Panen.objects.get(id_panen=id)
        panen_data.delete()
        return redirect('gudang-panen')

@gudang_required
def gudang_detail_mitra(request, id):
    mitra_detail = Mitra.objects.select_related('id_level_paket').all().filter(id_mitra=id)
    progress_budidaya_detail = ProgressBudidaya.objects.select_related('id_mitra').all()
    progress_budidaya_detail = progress_budidaya_detail.all().filter(id_mitra=id)
    hasil_panen_detail = Panen.objects.select_related('id_mitra').all()
    hasil_panen_detail = hasil_panen_detail.all().filter(id_mitra=id)

    if progress_budidaya_detail.exists() :
        mitra_identity = progress_budidaya_detail.first().id_mitra.nama_mitra
    if hasil_panen_detail.exists():
        mitra_identity = hasil_panen_detail.first().id_mitra.nama_mitra
    else:
        mitra_identity = mitra_detail.first().nama_mitra

    if mitra_detail.exists():
        mitra_tgl_registrasi = mitra_detail.first().tgl_registrasi
        mitra_tgl_registrasi = mitra_tgl_registrasi.strftime('%d %b %Y')
        mitra_periode_kontrak = mitra_detail.first().periode_kontrak
        mitra_level_paket = mitra_detail.first().id_level_paket
        mitra_kuota_cacing = mitra_detail.first().id_level_paket.kuota_cacing
        mitra_kuota_media_budidaya = mitra_detail.first().id_level_paket.kuota_media_budidaya
        mitra_kuota_panen = mitra_detail.first().id_level_paket.kuota_panen

    else:
        mitra_identity = ""


    return render(request, 'menu/gudang/gudang-detail_mitra.html', {
        "progress_budidaya_detail":progress_budidaya_detail, 
        "hasil_panen_detail":hasil_panen_detail, 
        "mitra_identity":mitra_identity,
        "mitra_tgl_registrasi": mitra_tgl_registrasi,
        "mitra_periode_kontrak": mitra_periode_kontrak,
        "mitra_level_paket": mitra_level_paket,
        "mitra_kuota_cacing": mitra_kuota_cacing,
        "mitra_kuota_panen": mitra_kuota_panen,
        "mitra_kuota_media_budidaya": mitra_kuota_media_budidaya
        })

@gudang_required
def gudang_list_mitra(request):

    progress_budidaya = ProgressBudidaya.objects.select_related('id_mitra').all().filter(
        tgl_pengamatan=Subquery(
            ProgressBudidaya.objects.filter(id_mitra=OuterRef('id_mitra')).order_by('-tgl_pengamatan').values('tgl_pengamatan')[:1]
        )
    ).distinct('id_mitra')
    panen = Panen.objects.select_related('id_mitra').all().filter(
        tgl_panen=Subquery(
            Panen.objects.filter(id_mitra=OuterRef('id_mitra')).order_by('-tgl_panen').values('tgl_panen')[:1]
        )
    ).distinct('id_mitra')

    mitra_query = Mitra.objects.prefetch_related(
        Prefetch('progressbudidaya_set', queryset=progress_budidaya, to_attr='all_progress_budidaya')
    ).filter(Q(progressbudidaya__isnull=True) | Q(progressbudidaya__in=progress_budidaya))

    mitra_query = mitra_query.prefetch_related(
        Prefetch('panen_set', queryset=panen, to_attr='all_panen')
    ).filter(Q(panen__isnull=True) | Q(panen__in=panen))

    return render(request, 'menu/gudang/gudang-list_mitra.html', {
        "mitra_query": mitra_query,
        })

"""
DESKRIPSI:
    View ini hanya dapat diakses oleh Role Owner
"""
@owner_required
def owner_dashboard(request):
    # Ini untuk grafik level paket
    paket_mitra_query = Mitra.objects.select_related('id_level_paket').all().order_by('id_level_paket__nama_paket')
    paket_mitra_query = paket_mitra_query.values('id_level_paket__nama_paket').annotate(count=Count('nama_mitra'))

    paket_mitra_labels = list(paket_mitra_query.values_list('id_level_paket__nama_paket', flat=True))
    paket_mitra_dataset = list(paket_mitra_query.values_list('count', flat=True))

    # Ini untuk card yang Total Mitra
    total_mitra = sum(paket_mitra_dataset)

    # Ini untuk grafik hasil panen
    panen = Panen.objects.all().order_by('tgl_panen')
    panen = panen.annotate(
        tahun_bulan=TruncMonth('tgl_panen'),
        tahun=ExtractYear('tgl_panen')).all()

    filter_panen = panen.values('tgl_panen').annotate(sum=Sum('berat_hasil_panen'))
    labels_panen = list(filter_panen.values_list('tgl_panen', flat=True))
    dataset_panen = list(filter_panen.values_list('sum', flat=True) )

    # Ini untuk card yang rata-rata panen per bulan
    # Perhitungan Rata-rata panen per bulan dilakukan melakukan pembagian antara kumulatif berat hasil panen keseluruhan dengan count unique MM-YYYY seluruh record data. Tapi apa benar seperti itu?. Atau pembagian nya jangan jangan menggunakan count unique year yang dikali 12?   
    kumulatif_berat_panen = sum(list(filter_panen.values_list('sum', flat=True)))
    jumlah_bulan = panen.values('tahun').distinct().count()
    if jumlah_bulan == 0:
        rata_rata_panen_per_bulan = 0
    else:
        rata_rata_panen_per_bulan = round(kumulatif_berat_panen / jumlah_bulan , 2)

    labels_panen_strings = []
    for date in labels_panen:
        labels_panen_strings.append(date.strftime('%Y-%m-%d'))
        
    return render(request, "menu/owner/owner-dashboard.html", {
        "labels_panen": labels_panen, 
        "dataset_panen": dataset_panen, 
        'labels_panen_strings':labels_panen_strings,
        "paket_mitra_query":paket_mitra_query,
        "paket_mitra_labels":paket_mitra_labels,
        "paket_mitra_dataset":paket_mitra_dataset,
        "total_mitra":total_mitra,
        "rata_rata_panen_per_bulan":rata_rata_panen_per_bulan
    })

@owner_required
def owner_list_mitra(request):
    mitra_query = Mitra.objects.all()
    return render(request, 'menu/owner/owner-list_mitra.html', {
        "mitra_query": mitra_query,
        })

@owner_required
def owner_laporan_target_produksi(request):
    mitra_query = Mitra.objects.all()
    return render(request, 'menu/owner/owner-target_produksi.html', {"mitra_query": mitra_query})

@owner_required
def owner_laporan_hasil_panen(request):
    panen_query = Panen.objects.select_related('id_mitra').all()
    panen_query = panen_query.select_related('id_mitra__id_level_paket').all()
    return render(request, 'menu/owner/owner-hasil_panen.html', {"panen_query": panen_query})

@owner_required
def owner_rekapitulasi_target_dan_realisasi(request):
    mitra_query = Mitra.objects.all()

    panen = Panen.objects.select_related('id_mitra').all()

    panen_query = Mitra.objects.prefetch_related(
        Prefetch('panen_set', queryset=panen, to_attr='all_panen')
    ).filter(Q(panen__isnull=True) | Q(panen__in=panen))

    produktivitas_panen_query = panen_query.values('id_mitra').annotate(
        total_berat_hasil_panen=Sum('panen__berat_hasil_panen'),
        nama_mitra = ExpressionWrapper(
            F('nama_mitra'), CharField()
        ),

        item_cacing = ExpressionWrapper(
            F('id_level_paket__kuota_cacing'), CharField()
        ),
        kuota_panen = ExpressionWrapper(
            F('id_level_paket__kuota_panen'), CharField()
        )
    )

    produktivitas_panen_query = produktivitas_panen_query.annotate(
        produktivitas = ExpressionWrapper(
            Cast(F('total_berat_hasil_panen'), FloatField())/
            Cast(F('id_level_paket__kuota_cacing'), FloatField())
            * 100
            , 
            output_field=IntegerField()),
    )

    nihil_panen = produktivitas_panen_query.filter(total_berat_hasil_panen__isnull = True)
    nihil_panen = nihil_panen.count()

    kumulatif_berat_panen = Panen.objects.annotate(sum=Sum('berat_hasil_panen'))
    kumulatif_berat_panen = sum(list(kumulatif_berat_panen.values_list('sum', flat=True)))

    low_productivity = produktivitas_panen_query.filter(produktivitas__lt = 100).count()
    low_productivity = low_productivity + nihil_panen
    good_productivity = produktivitas_panen_query.filter(produktivitas__gte = 100).count()

    top_ten_query = produktivitas_panen_query.filter(total_berat_hasil_panen__isnull = False)
    top_ten_query = top_ten_query.order_by('-produktivitas')[:10]
    
    return render(request, 'menu/owner/owner-target_realisasi.html', {
        "produktivitas_panen_query": produktivitas_panen_query,
        "nihil_panen": nihil_panen,
        "kumulatif_berat_panen": kumulatif_berat_panen,
        "low_productivity": low_productivity,
        "good_productivity": good_productivity,
        "top_ten_query": top_ten_query
        })

@owner_required
def owner_detail_mitra(request, id):
    mitra_detail = Mitra.objects.all().filter(id_mitra=id)
    panen_detail = Panen.objects.select_related('id_mitra').all()
    panen_detail = panen_detail.all().filter(id_mitra=id)

    progress_budidaya_detail = ProgressBudidaya.objects.select_related('id_mitra').all()
    progress_budidaya_detail = progress_budidaya_detail.all().filter(id_mitra=id)

    if progress_budidaya_detail.exists():
        mitra_identity = progress_budidaya_detail.first().id_mitra.nama_mitra
    elif panen_detail.exists():
        mitra_identity = panen_detail.first().id_mitra.nama_mitra
    else:
        mitra_identity = mitra_detail.first().nama_mitra

    if mitra_detail.exists():
        mitra_alamat = mitra_detail.first().alamat
        mitra_pendidikan = mitra_detail.first().pendidikan
        mitra_pelatihan = mitra_detail.first().pelatihan
        mitra_tgl_lahir = mitra_detail.first().tgl_lahir
        mitra_tgl_lahir_str = mitra_tgl_lahir.strftime('%d %b %Y')
        mitra_pengalaman_kerja = mitra_detail.first().pengalaman_budidaya
        mitra_motivasi_bermitra = mitra_detail.first().motivasi_bermitra
        mitra_periode_kontrak = mitra_detail.first().periode_kontrak
        mitra_tgl_registrasi = mitra_detail.first().tgl_registrasi
        mitra_level_paket = mitra_detail.first().id_level_paket
        mitra_jenis_kelamin = mitra_detail.first().jenis_kelamin
        mitra_no_hp = mitra_detail.first().no_hp

    else:
        mitra_identity = ""

    return render(request, 'menu/owner/owner-detail_mitra.html', {
        "mitra_detail":mitra_detail, 
        "panen_detail":panen_detail, 
        "progress_budidaya_detail":progress_budidaya_detail, 
        "mitra_identity":mitra_identity, 
        "mitra_alamat":mitra_alamat,
        "mitra_pendidikan":mitra_pendidikan,
        "mitra_pelatihan":mitra_pelatihan,
        "mitra_tgl_lahir":mitra_tgl_lahir_str,
        "mitra_pengalaman_kerja":mitra_pengalaman_kerja,
        "mitra_motivasi_bermitra":mitra_motivasi_bermitra,
        "mitra_periode_kontrak":mitra_periode_kontrak,
        "mitra_tgl_registrasi":mitra_tgl_registrasi,
        "mitra_level_paket":mitra_level_paket,
        "mitra_jenis_kelamin":mitra_jenis_kelamin,
        "mitra_no_hp":mitra_no_hp,

       })

@owner_required
def owner_faq(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_faq')         
    else:
        form = FAQForm()

    faq_query = FAQ.objects.all()
    return render(request, 'menu/owner/owner-faq.html', {
        "faq_query": faq_query,
        'form': form}
        )

@owner_required
def owner_faq_update(request, id):
    faq_data = FAQ.objects.get(id_faq=id)
    faq_model = get_object_or_404(FAQ, id_faq=id)
    form = FAQForm(request.POST or None, instance=faq_model)
    if form.is_valid():
        form.save()
        return redirect('owner_faq')
    return render(request, 'menu/owner/owner-faq_update.html', {
        "faq_model":faq_model, 
        "form": form,
        "faq_data": faq_data,
        })

@owner_required
def owner_faq_delete(request, id):
        faq_data = FAQ.objects.get(id_faq=id)
        faq_data.delete()
        return redirect('owner_faq')


@owner_required
def owner_pelatihan(request):
    if request.method == 'POST':
        form = PelatihanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_pelatihan')            
    else:
        form = PelatihanForm()

    pelatihan_query = Pelatihan.objects.all()
    return render(request, 'menu/owner/owner-pelatihan.html', {
        "pelatihan_query": pelatihan_query,
        'form': form}
        )

@owner_required
def owner_pelatihan_update(request, id):
    pelatihan_data = Pelatihan.objects.get(id_pelatihan=id)
    pelatihan_model = get_object_or_404(Pelatihan, id_pelatihan=id)
    form = PelatihanForm(request.POST or None, instance=pelatihan_model)
    if form.is_valid():
        form.save()
        return redirect('owner_pelatihan')
    return render(request, 'menu/owner/owner-pelatihan_update.html', {
        "pelatihan_model":pelatihan_model, 
        "form": form,
        "pelatihan_data": pelatihan_data,
        })

@owner_required
def owner_pelatihan_delete(request, id):
    pelatihan_data = Pelatihan.objects.get(id_pelatihan=id)
    pelatihan_data.delete()
    return redirect('owner_pelatihan')


@owner_required
def owner_record_progress_budidaya(request):
    progress_budidaya_detail = ProgressBudidaya.objects.select_related('id_mitra').all()

    return render(request, 'menu/owner/owner-record_progress_budidaya.html', {
        "progress_budidaya_detail":progress_budidaya_detail
       })