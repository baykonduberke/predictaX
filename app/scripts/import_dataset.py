"""
Dataset Import Script
Matches.csv dosyasından veritabanına veri aktarır.

Kullanım:
    # Tüm verileri import et (divisions, teams, matches, elo_history)
    python -m app.scripts.import_dataset --db "postgresql://user:pass@localhost:5432/dbname"
    
    # Sadece belirli kısımları import et
    python -m app.scripts.import_dataset --db "..." --only matches
    python -m app.scripts.import_dataset --db "..." --only elo
    python -m app.scripts.import_dataset --db "..." --only teams
"""

import argparse
import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models import Division, Team, Match, MatchResult, EloHistory


def safe_int(value):
    """NaN değerlerini None'a çevir."""
    if pd.isna(value):
        return None
    return int(value)


def safe_float(value):
    """NaN değerlerini None'a çevir."""
    if pd.isna(value):
        return None
    return float(value)


def get_session(database_url: str):
    """Database session oluştur."""
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def import_divisions(db, df) -> dict:
    """Division'ları import et ve mapping döndür."""
    print("\n🏆 Division'lar oluşturuluyor...")
    divisions = df['Division'].unique()
    div_map = {}
    
    for code in divisions:
        existing = db.query(Division).filter(Division.code == code).first()
        if existing:
            div_map[code] = existing.id
        else:
            div = Division(code=code, name=code)
            db.add(div)
            db.flush()
            div_map[code] = div.id
    
    db.commit()
    print(f"   ✅ {len(divisions)} division eklendi/güncellendi")
    return div_map


def import_teams(db, df) -> dict:
    """Takımları import et ve mapping döndür."""
    print("\n⚽ Takımlar oluşturuluyor...")
    home_teams = set(df['HomeTeam'].unique())
    away_teams = set(df['AwayTeam'].unique())
    all_teams = home_teams | away_teams
    
    team_map = {}
    for name in all_teams:
        existing = db.query(Team).filter(Team.name == name).first()
        if existing:
            team_map[name] = existing.id
        else:
            team = Team(name=name)
            db.add(team)
            db.flush()
            team_map[name] = team.id
    
    db.commit()
    print(f"   ✅ {len(all_teams)} takım eklendi/güncellendi")
    return team_map


def import_matches(db, df, div_map: dict, team_map: dict, batch_size: int = 1000):
    """Maçları import et."""
    total_rows = len(df)
    print(f"\n📅 Maçlar ekleniyor ({batch_size} satırlık batch'ler)...")
    
    matches_added = 0
    matches_skipped = 0
    
    for i, row in df.iterrows():
        match_date = pd.to_datetime(row['MatchDate']).date()
        home_team_id = team_map[row['HomeTeam']]
        away_team_id = team_map[row['AwayTeam']]
        
        existing = db.query(Match).filter(
            Match.match_date == match_date,
            Match.home_team_id == home_team_id,
            Match.away_team_id == away_team_id
        ).first()
        
        if existing:
            matches_skipped += 1
            continue
        
        match_time = None
        if pd.notna(row.get('MatchTime')) and row.get('MatchTime'):
            try:
                match_time = pd.to_datetime(row['MatchTime']).time()
            except:
                pass
        
        ft_result = None
        if pd.notna(row.get('FTResult')) and row.get('FTResult') in ['H', 'D', 'A']:
            ft_result = MatchResult(row['FTResult'])
        
        ht_result = None
        if pd.notna(row.get('HTResult')) and row.get('HTResult') in ['H', 'D', 'A']:
            ht_result = MatchResult(row['HTResult'])
        
        match = Match(
            division_id=div_map[row['Division']],
            match_date=match_date,
            match_time=match_time,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            home_team_elo=safe_float(row.get('HomeElo')),
            away_team_elo=safe_float(row.get('AwayElo')),
            form3_home=safe_int(row.get('Form3Home')),
            form3_away=safe_int(row.get('Form3Away')),
            form5_home=safe_int(row.get('Form5Home')),
            form5_away=safe_int(row.get('Form5Away')),
            ft_home=safe_int(row.get('FTHome')),
            ft_away=safe_int(row.get('FTAway')),
            ft_result=ft_result,
            ht_home=safe_int(row.get('HTHome')),
            ht_away=safe_int(row.get('HTAway')),
            ht_result=ht_result,
            home_shots=safe_int(row.get('HomeShots')),
            away_shots=safe_int(row.get('AwayShots')),
            home_shots_target=safe_int(row.get('HomeTarget')),
            away_shots_target=safe_int(row.get('AwayTarget')),
            home_corners=safe_int(row.get('HomeCorners')),
            away_corners=safe_int(row.get('AwayCorners')),
            home_fouls=safe_int(row.get('HomeFouls')),
            away_fouls=safe_int(row.get('AwayFouls')),
            home_yellow=safe_int(row.get('HomeYellow')),
            away_yellow=safe_int(row.get('AwayYellow')),
            home_red=safe_int(row.get('HomeRed')),
            away_red=safe_int(row.get('AwayRed')),
            odd_home=safe_float(row.get('OddHome')),
            odd_draw=safe_float(row.get('OddDraw')),
            odd_away=safe_float(row.get('OddAway')),
            odd_over25=safe_float(row.get('Over25')),
            odd_under25=safe_float(row.get('Under25')),
            c_htb=safe_float(row.get('C_HTB')),
            c_phb=safe_float(row.get('C_PHB')),
            c_vhd=safe_float(row.get('C_VHD')),
            c_vad=safe_float(row.get('C_VAD')),
            c_lth=safe_float(row.get('C_LTH')),
            c_lta=safe_float(row.get('C_LTA')),
            source='csv'
        )
        db.add(match)
        matches_added += 1
        
        if matches_added % batch_size == 0:
            db.commit()
            progress = ((i + 1) / total_rows) * 100
            print(f"   📈 İlerleme: {progress:.1f}% ({matches_added:,} eklendi, {matches_skipped:,} atlandı)")
    
    db.commit()
    print(f"   ✅ Maçlar: {matches_added:,} eklendi, {matches_skipped:,} atlandı")
    return matches_added, matches_skipped


def import_elo_history(db, df, team_map: dict, batch_size: int = 5000):
    """ELO history verilerini import et."""
    total_rows = len(df)
    print(f"\n📈 ELO History oluşturuluyor...")
    
    # ELO kayıtlarını topla (set ile duplicate önle)
    elo_records = set()
    
    for i, row in df.iterrows():
        match_date = pd.to_datetime(row['MatchDate']).date()
        
        # Home team ELO
        home_team = row['HomeTeam']
        home_elo = row.get('HomeElo')
        if home_team in team_map and pd.notna(home_elo):
            elo_records.add((team_map[home_team], match_date, float(home_elo)))
        
        # Away team ELO
        away_team = row['AwayTeam']
        away_elo = row.get('AwayElo')
        if away_team in team_map and pd.notna(away_elo):
            elo_records.add((team_map[away_team], match_date, float(away_elo)))
        
        if (i + 1) % 50000 == 0:
            print(f"   📊 {i + 1:,}/{total_rows:,} maç işlendi...")
    
    print(f"   📊 {len(elo_records):,} benzersiz ELO kaydı bulundu")
    
    # Database'e ekle
    added = 0
    skipped = 0
    records_list = list(elo_records)
    
    for i, (team_id, date, elo) in enumerate(records_list):
        existing = db.query(EloHistory).filter(
            EloHistory.team_id == team_id,
            EloHistory.date == date
        ).first()
        
        if existing:
            skipped += 1
            continue
        
        db.add(EloHistory(team_id=team_id, date=date, elo=elo))
        added += 1
        
        if added % batch_size == 0:
            db.commit()
            progress = ((i + 1) / len(records_list)) * 100
            print(f"   📈 İlerleme: {progress:.1f}% ({added:,} eklendi, {skipped:,} atlandı)")
    
    db.commit()
    print(f"   ✅ ELO History: {added:,} eklendi, {skipped:,} atlandı")
    return added, skipped


def run_import(csv_path: str, database_url: str, only: str = None):
    """
    Ana import fonksiyonu.
    
    Args:
        csv_path: CSV dosyasının yolu
        database_url: PostgreSQL bağlantı URL'si
        only: Sadece belirli bir kısmı import et (teams, matches, elo, None=hepsi)
    """
    print("=" * 60)
    print("🚀 PredictaX Dataset Import")
    print("=" * 60)
    
    print(f"\n📂 CSV okunuyor: {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)
    total_rows = len(df)
    print(f"📊 Toplam {total_rows:,} satır bulundu")
    
    print(f"\n🔗 Database'e bağlanılıyor...")
    db = get_session(database_url)
    print(f"   ✅ Bağlantı başarılı")
    
    try:
        # Division ve Team her zaman gerekli (mapping için)
        if only in [None, 'teams', 'matches']:
            div_map = import_divisions(db, df)
            team_map = import_teams(db, df)
        else:
            # Sadece elo için mevcut team'leri yükle
            print("\n⚽ Mevcut takımlar yükleniyor...")
            teams = db.query(Team).all()
            team_map = {team.name: team.id for team in teams}
            print(f"   ✅ {len(team_map)} takım yüklendi")
            div_map = {}
        
        # Matches
        if only in [None, 'matches']:
            import_matches(db, df, div_map, team_map)
        
        # ELO History
        if only in [None, 'elo']:
            import_elo_history(db, df, team_map)
        
        print("\n" + "=" * 60)
        print("✅ IMPORT TAMAMLANDI!")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ HATA: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Matches.csv'den veritabanına veri import et",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  # Tüm verileri import et
  python -m app.scripts.import_dataset --db "postgresql://postgres:sifre123@localhost:5432/predictax"
  
  # Sadece maçları import et
  python -m app.scripts.import_dataset --db "..." --only matches
  
  # Sadece ELO history import et
  python -m app.scripts.import_dataset --db "..." --only elo
        """
    )
    parser.add_argument(
        "--db", 
        type=str, 
        help="PostgreSQL URL (örn: postgresql://user:pass@localhost:5432/predictax)"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="CSV dosya yolu (varsayılan: app/data/Matches.csv)"
    )
    parser.add_argument(
        "--only",
        type=str,
        choices=['teams', 'matches', 'elo'],
        default=None,
        help="Sadece belirli bir kısmı import et"
    )
    args = parser.parse_args()
    
    # Database URL
    db_url = args.db or os.getenv("DATABASE_URL_SYNC")
    if not db_url:
        print("❌ Database URL gerekli!")
        print("   --db argümanı ile ver veya DATABASE_URL_SYNC ortam değişkeni ayarla")
        print("\n   Örnek:")
        print('   python -m app.scripts.import_dataset --db "postgresql://postgres:sifre123@localhost:5432/predictax"')
        exit(1)
    
    # CSV path
    if args.csv:
        csv_path = Path(args.csv)
    else:
        csv_path = Path(__file__).parent.parent / "data" / "Matches.csv"
    
    if not csv_path.exists():
        print(f"❌ CSV dosyası bulunamadı: {csv_path}")
        exit(1)
    
    run_import(str(csv_path), db_url, args.only)
