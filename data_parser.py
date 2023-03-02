def diskusiparser(arr):
    hasil = []
    jenis = hasil.append(arr[1])
    jurusan = hasil.append(arr[3])
    matkul = hasil.append(arr[4])
    dosen = hasil.append(arr[5])

    indikatorkemampuan = arr[arr.index(
        'Indikator Kemampuan :') + 1: arr.index('Materi Perkuliahan :')]

    hasil.append(" | ".join(indikatorkemampuan))
    materiperkuliahan = arr[arr.index('Materi Perkuliahan :')+1:arr.index('Bentuk Pembelajaran :')]
    hasil.append(" | ".join(materiperkuliahan))
    bentuk_pembelajaran = arr[arr.index('Bentuk Pembelajaran :') + 1:arr.index('Bentuk Pembelajaran :')+2]
    hasil.append(" | ".join(bentuk_pembelajaran))
    desc = arr[arr.index('Bentuk Pembelajaran :') +2:arr.index('Waktu Mulai')]
    matches = []

    for match in desc:
        if ".com" in match:
            matches.append(match)

    for popup in matches:
        desc.pop(desc.index(popup))
    hasil.append(" | ".join(desc))
    return hasil
