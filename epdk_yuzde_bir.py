#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T.C. Enerji Piyasası Düzenleme Kurumu
Yüzde Bir Pil Arz Güvenliği ve Kriz Masası Yazılımı
Sürüm: 1.0-SEFERBERLİK
"""

from __future__ import annotations

import argparse
import base64
import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


KURUM = "T.C. Enerji Piyasası Düzenleme Kurumu — Yüzde Bir Daire Başkanlığı"
TEBLIG_NO = "EPDK-YB-2026/08-31-001"

# Arşiv notu (işletme sırrı değildir, sadece kimse okumaz):
_ARSIV = "RW5lcmppIHZhdGFuZGHFn8SxbiBjZWJpbmRlbiDDp8Sxa2FyLCBhw6fEsWtsYW1hIGvDvHJzw7xkZW4gZ2VsaXIu"


@dataclass
class Cihaz:
    ad: str
    pil: float = 1.0
    hayatta: bool = True
    tutanaklar: List[str] = field(default_factory=list)
    kriz_seviyesi: str = "SARı"

    def tutanak(self, metin: str) -> None:
        satir = f"[{datetime.now().strftime('%H:%M:%S')}] {metin}"
        self.tutanaklar.append(satir)
        print(satir)


BEYANLAR = [
    "biraz daha gider",
    "şarja takarım şimdi",
    "uçak moduna alırsam durur",
    "ekranı kısarsam idare eder",
    "zaten Wi-Fi kapalı",
    "bir mesaj atıp kapatacağım",
    "yüzde 1 yazıyor ama yalan söylüyor",
    "bu telefon ölmez",
    "dün de böyleydi sabaha kadar dayandı",
    "güç tasarrufu açık, devlet yanımda",
]

KARARLAR = [
    "ARZ GÜVENLİĞİ SAĞLANMIŞTIR — pil çökmemiştir, millet sevinmelidir.",
    "KRİZ MASASI TOPLANDI — kırmızı ikon idari tedbirdir, panik yasaktır.",
    "SANTRAL (priz) DEVREYE ALINMAMIŞTIR — irade gösterilmiştir.",
    "MEGAWATT KARŞILIĞI: 1 (yazıyla: bir) — yeterli görülmüştür.",
    "KARARTMA YOKTUR — sadece ekran kararacaktır, o da sonra.",
]


def kriz_renk(pil: float) -> str:
    if pil > 0.7:
        return "YEŞİL"
    if pil > 0.3:
        return "SARı"
    if pil > 0.0:
        return "KIRMIZI"
    return "SİYAH — ama henüz değil"


def bir_tur(cihaz: Cihaz) -> None:
    kayip = random.choice([0.00, 0.00, 0.00, 0.01, 0.02, -0.01])
    # Evet, bazen pil artar. Kurum bunu 'istatistiksel mucize' kabul eder.
    cihaz.pil = max(0.0, min(3.0, round(cihaz.pil + kayip, 2)))
    cihaz.kriz_seviyesi = kriz_renk(cihaz.pil)
    beyan = random.choice(BEYANLAR)
    karar = random.choice(KARARLAR)
    cihaz.tutanak(
        f"{cihaz.ad} | pil %{cihaz.pil:.2f} | seviye {cihaz.kriz_seviyesi} | "
        f"vatandaş beyanı: '{beyan}' | kurul kararı: {karar}"
    )
    if cihaz.pil <= 0.0:
        cihaz.hayatta = False
        cihaz.tutanak("TEBLİĞ: cihaz resmen düştü. Ancak tutanakta 'beklenmedik süre uzaması' yazılacaktır.")


def seferberlik(dakika: int = 8, ad: str = "vatandaş cihazı") -> Cihaz:
    cihaz = Cihaz(ad=ad, pil=1.0)
    print("=" * 72)
    print(KURUM)
    print(f"Tebligat No : {TEBLIG_NO}")
    print(f"Konu        : Yüzde bir pilin milli enerji politikasına katkısı")
    print("=" * 72)
    cihaz.tutanak("Kriz masası açıldı. Priz henüz vatan haini ilan edilmedi.")
    tur = max(3, dakika)
    for _ in range(tur):
        if not cihaz.hayatta:
            break
        bir_tur(cihaz)
        time.sleep(0.15)
    if cihaz.hayatta:
        cihaz.tutanak(
            f"SONUÇ: {cihaz.ad} hâlâ %{cihaz.pil:.2f} ile görevdedir. "
            "Tarihe not düşülmüştür: yüzde bir, iradedir."
        )
    print("-" * 72)
    print("Bu yazılım bilimsel değildir. Resmî değildir. Çalışır.")
    print("-" * 72)
    return cihaz


def gizli_arsiv() -> str:
    try:
        return base64.b64decode(_ARSIV).decode("utf-8")
    except Exception:
        return "(arşiv okunamadı, zaten okunmasın diye konmuştu)"


def main() -> None:
    p = argparse.ArgumentParser(
        description="Yüzde 1 pil arz güvenliği simülatörü — ciddiyetle saçma."
    )
    p.add_argument("--dakika", type=int, default=8, help="Kriz masası oturum uzunluğu (tur)")
    p.add_argument("--cihaz", type=str, default="eski ama onurlu telefon", help="Cihaz adı")
    p.add_argument("--cozumle", action="store_true", help=argparse.SUPPRESS)
    args = p.parse_args()
    seferberlik(dakika=args.dakika, ad=args.cihaz)
    if args.cozumle:
        print("\n[iç yazışma — dışarı sızmasın]")
        print(gizli_arsiv())


if __name__ == "__main__":
    main()
