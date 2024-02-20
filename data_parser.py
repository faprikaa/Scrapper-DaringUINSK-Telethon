def diskusi_parser(arr):
    hasil = []
    jenis = hasil.append(arr[1])
    jurusan = hasil.append(arr[3])
    matkul = hasil.append(arr[4])
    dosen = hasil.append(arr[5])

    indikatorkemampuan = arr[arr.index(
        'Indikator Kemampuan :') + 1: arr.index('Materi Perkuliahan :')]

    hasil.append(" | ".join(indikatorkemampuan))
    materiperkuliahan = arr[arr.index(
        'Materi Perkuliahan :') + 1:arr.index('Bentuk Pembelajaran :')]
    hasil.append(" | ".join(materiperkuliahan))
    bentuk_pembelajaran = arr[arr.index(
        'Bentuk Pembelajaran :') + 1:arr.index('Bentuk Pembelajaran :') + 2]
    hasil.append(" | ".join(bentuk_pembelajaran))
    desc = arr[arr.index('Bentuk Pembelajaran :') + 2:arr.index('Waktu Mulai')]

    if arr.index('Waktu Mulai') > arr.index('|'):
        desc = arr[arr.index('Bentuk Pembelajaran :') + 2:arr.index('|') - 1]
    elif arr.index('Waktu Mulai') < arr.index('|'):
        desc = arr[arr.index('Bentuk Pembelajaran :') +
                   2:arr.index('Waktu Mulai')]
    else:
        print("diskuparser:", arr.index('Waktu Mulai'), arr.index('|'))

    matches = []
    link = ['http://', 'https://']
    for match in desc:
        for links in link:
            if links in match:
                matches.append(match)

    for popup in matches:
        desc.pop(desc.index(popup))

    desct = []
    desct.append(" | ".join(desc))

    if (len(desct[0]) > 450):
        hasil.append(desct[0][:450])
    else:
        hasil.append(" | ".join(desc))

    waktu_mulai = arr[arr.index('Waktu Mulai') + 1]
    hasil.append(waktu_mulai)

    waktu_selesai = arr[arr.index('Waktu Selesai') + 1]
    hasil.append(waktu_selesai)
    return hasil


def forum_parser(arr):
    hasil = []
    jenis = hasil.append(arr[0])
    jurusan = hasil.append(arr[2])
    matkul = hasil.append(arr[3])
    pengirim = hasil.append(arr[1])

    desc = arr[4:arr.index('setuju') - 3]
    matches = []

    for match in desc:
        if ".com" in match:
            matches.append(match)

    for popup in matches:
        desc.pop(desc.index(popup))
    hasil.append(" | ".join(desc))
    return hasil


def materi_parser(arr):
    hasil = []
    jenis = hasil.append(arr[0])
    dosen = hasil.append(arr[1])
    jurusan = hasil.append(arr[2])
    matkul = hasil.append(arr[3])

    deskripsi = arr[4: arr.index('|') - 1]
    hasil.append(" | ".join(deskripsi))

    return hasil


def meeting_parser(arr):
    hasil = []
    jenis = hasil.append(arr[1])
    jurusan = hasil.append(arr[3])
    matkul = hasil.append(arr[4])
    dosen = hasil.append(arr[5])

    indikatorkemampuan = arr[arr.index(
        'Indikator Kemampuan :') + 1: arr.index('Materi Perkuliahan :')]
    hasil.append(" | ".join(indikatorkemampuan))

    materiperkuliahan = arr[arr.index(
        'Materi Perkuliahan :') + 1: arr.index('Bentuk Pembelajaran :')]
    hasil.append(" | ".join(materiperkuliahan))

    bentuk_pembelajaran = arr[arr.index('Bentuk Pembelajaran :') + 1]
    hasil.append(bentuk_pembelajaran)

    if arr.index('Waktu Mulai') > arr.index('|'):
        desc = arr[arr.index('Bentuk Pembelajaran :') + 2:arr.index('|') - 1]
    elif arr.index('Waktu Mulai') < arr.index('|'):
        desc = arr[arr.index('Bentuk Pembelajaran :') +
                   2:arr.index('Waktu Mulai')]
    else:
        print("metingparser:", arr.index('Waktu Mulai'), arr.index('|'))

    matches = []
    for match in desc:
        if ".com" in match:
            matches.append(match)
    hasil.append(" | ".join(matches))

    for popup in matches:
        desc.pop(desc.index(popup))
    hasil.append(" | ".join(desc))

    waktu_mulai = arr[arr.index('Waktu Mulai') + 1]
    hasil.append(waktu_mulai)

    waktu_selesai = arr[arr.index('Waktu Selesai') + 1]
    hasil.append(waktu_selesai)

    return hasil


def video_parser(arr):
    hasil = []
    jenis = hasil.append(arr[1] + " | " + arr[2])
    jurusan = hasil.append(arr[3])
    matkul = hasil.append(arr[4])
    dosen = hasil.append(arr[5])

    indikatorkemampuan = arr[arr.index(
        'Indikator Kemampuan :') + 1: arr.index('Materi Perkuliahan :')]
    hasil.append(" | ".join(indikatorkemampuan))

    materiperkuliahan = arr[arr.index(
        'Materi Perkuliahan :') + 1: arr.index('Bentuk Pembelajaran :')]
    hasil.append(" | ".join(materiperkuliahan))

    bentuk_pembelajaran = arr[arr.index('Bentuk Pembelajaran :') + 1]
    hasil.append(bentuk_pembelajaran)

    if arr.index('Waktu Mulai') > arr.index('|'):
        desc = arr[arr.index('Putar hanya audio') + 1:arr.index('|') - 1]
    elif arr.index('Waktu Mulai') < arr.index('|'):
        desc = arr[arr.index('Putar hanya audio') + 1:arr.index('Waktu Mulai')]
    else:
        desc = " "
        print("metingparser:", arr.index('Waktu Mulai'), arr.index('|'))
    hasil.append(" | ".join(desc))

    waktu_mulai = arr[arr.index('Waktu Mulai') + 1]
    hasil.append(waktu_mulai)

    waktu_selesai = arr[arr.index('Waktu Selesai') + 1]
    hasil.append(waktu_selesai)

    return hasil


def tugas_parser(arr):
    hasil = []
    jenis = hasil.append(arr[0] + " | " + arr[1])
    jurusan = hasil.append(arr[2])
    matkul = hasil.append(arr[3])
    dosen = hasil.append(arr[4])

    if arr.index('Waktu Mulai') > arr.index('|'):
        desc = arr[5:arr.index('|') - 1]
    elif arr.index('Waktu Mulai') < arr.index('|'):
        desc = arr[5:arr.index('Waktu Mulai')]
    else:
        print("tugasparser:", arr.index('Waktu Mulai'), arr.index('|'))
    hasil.append(" | ".join(desc))

    waktu_mulai = arr[arr.index('Waktu Mulai') + 1]
    hasil.append(waktu_mulai)

    waktu_selesai = arr[arr.index('Waktu Selesai') + 1]
    hasil.append(waktu_selesai)

    return hasil


def pengumuman_parser(arr):
    hasil = []
    jenis = hasil.append(arr[0])
    jurusan = hasil.append(arr[2])
    matkul = hasil.append(arr[3])
    dosen = hasil.append(arr[1])

    desc = arr[3:arr.index('setuju') - 1]
    hasil.append(" | ".join(desc))

    return hasil
