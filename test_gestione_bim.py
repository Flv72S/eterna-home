#!/usr/bin/env python3
"""
Script di test per le funzionalità BIM di Eterna-Home.
Testa il caricamento, la gestione e le operazioni sui modelli BIM.
"""

import requests
import json
import os
import tempfile
from datetime import datetime

# Configurazione
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Credenziali di test
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin123"

class BIMAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.test_user_id = None
        self.test_house_id = None
        self.test_bim_model_id = None
    
    def login(self):
        """Effettua il login e ottiene il token di accesso."""
        print("🔐 Effettuando login...")
        
        login_data = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
        
        response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
            print("✅ Login effettuato con successo")
            return True
        else:
            print(f"❌ Login fallito: {response.status_code} - {response.text}")
            return False
    
    def get_test_data(self):
        """Ottiene dati di test (utente, casa) per i test."""
        print("📋 Ottenendo dati di test...")
        
        # Ottieni utente corrente
        response = self.session.get(f"{API_BASE}/users/me")
        if response.status_code == 200:
            user_data = response.json()
            self.test_user_id = user_data["id"]
            print(f"✅ Utente di test: {user_data['username']} (ID: {self.test_user_id})")
        
        # Ottieni case dell'utente
        response = self.session.get(f"{API_BASE}/houses/")
        if response.status_code == 200:
            houses = response.json()["items"]
            if houses:
                self.test_house_id = houses[0]["id"]
                print(f"✅ Casa di test: {houses[0]['name']} (ID: {self.test_house_id})")
    
    def create_test_bim_file(self, format_type="ifc"):
        """Crea un file BIM di test."""
        # Crea un file temporaneo con contenuto di test
        content = f"""# Test BIM Model
# Format: {format_type.upper()}
# Created: {datetime.now()}
# Description: Test model for Eterna-Home

ENTITY IfcProject (
    GlobalId := '2O2Fr$t4X7Zf8NOew3FNrX';
    Name := 'Test Project';
    Description := 'Test BIM model for Eterna-Home';
    ObjectType := 'Project';
    LongName := 'Test Project for BIM Management';
    Phase := 'DESIGN';
    RepresentationContexts := (#);
    UnitsInContext := #;
);
END_ENTITY;

ENTITY IfcBuilding (
    GlobalId := '3O2Fr$t4X7Zf8NOew3FNrY';
    Name := 'Test Building';
    Description := 'Test building for Eterna-Home';
    ObjectType := 'Building';
    LongName := 'Test Building for BIM Management';
    CompositionType := ELEMENT;
    ElevationOfRefHeight := 0.0;
);
END_ENTITY;
"""
        
        # Crea file temporaneo
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{format_type}', delete=False) as f:
            f.write(content)
            temp_file_path = f.name
        
        return temp_file_path
    
    def test_upload_bim_model(self):
        """Test: Upload modello BIM."""
        print("\n🧪 Test: Upload modello BIM")
        
        if not self.test_house_id:
            print("⚠️  Nessuna casa disponibile per il test")
            return False
        
        # Crea file di test
        test_file_path = self.create_test_bim_file("ifc")
        
        try:
            with open(test_file_path, 'rb') as f:
                files = {'file': ('test_model.ifc', f, 'application/octet-stream')}
                data = {
                    'name': 'Test BIM Model',
                    'description': 'Modello di test per Eterna-Home'
                }
                
                response = self.session.post(
                    f"{API_BASE}/bim/upload",
                    files=files,
                    data=data
                )
            
            # Pulisci file temporaneo
            os.unlink(test_file_path)
            
            if response.status_code == 201:
                data = response.json()
                self.test_bim_model_id = data["id"]
                print(f"✅ Modello BIM caricato: ID {data['id']}")
                print(f"   Nome: {data['name']}")
                print(f"   Formato: {data['format']}")
                print(f"   Dimensione: {data['file_size']} bytes")
                return True
            else:
                print(f"❌ Errore upload: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Errore durante upload: {e}")
            return False
    
    def test_get_bim_models(self):
        """Test: Lista modelli BIM."""
        print("\n🧪 Test: Lista modelli BIM")
        
        response = self.session.get(f"{API_BASE}/bim/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Modelli BIM trovati: {data['total']}")
            print(f"   Pagina: {data['page']}/{data['pages']}")
            print(f"   Elementi per pagina: {data['size']}")
            
            if data["items"]:
                model = data["items"][0]
                print(f"   Primo modello: {model['name']} ({model['format']})")
            
            return True
        else:
            print(f"❌ Errore: {response.status_code} - {response.text}")
            return False
    
    def test_get_bim_model_by_id(self):
        """Test: Modello BIM specifico."""
        print("\n🧪 Test: Modello BIM specifico")
        
        if not self.test_bim_model_id:
            print("⚠️  Nessun modello BIM disponibile per il test")
            return False
        
        response = self.session.get(f"{API_BASE}/bim/{self.test_bim_model_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Modello BIM trovato: ID {data['id']}")
            print(f"   Nome: {data['name']}")
            print(f"   Formato: {data['format']}")
            print(f"   Software: {data['software_origin']}")
            print(f"   LOD: {data['level_of_detail']}")
            return True
        else:
            print(f"❌ Errore: {response.status_code} - {response.text}")
            return False
    
    def test_bim_formats(self):
        """Test: Formati BIM supportati."""
        print("\n🧪 Test: Formati BIM supportati")
        
        # Test diversi formati
        formats = ["ifc", "rvt", "dwg", "dxf", "skp", "pln"]
        
        for fmt in formats:
            test_file_path = self.create_test_bim_file(fmt)
            
            try:
                with open(test_file_path, 'rb') as f:
                    files = {'file': (f'test_model.{fmt}', f, 'application/octet-stream')}
                    data = {'name': f'Test {fmt.upper()} Model'}
                    
                    response = self.session.post(
                        f"{API_BASE}/bim/upload",
                        files=files,
                        data=data
                    )
                
                os.unlink(test_file_path)
                
                if response.status_code == 201:
                    print(f"✅ Formato {fmt.upper()}: supportato")
                else:
                    print(f"❌ Formato {fmt.upper()}: non supportato ({response.status_code})")
                    
            except Exception as e:
                print(f"❌ Errore formato {fmt}: {e}")
                os.unlink(test_file_path)
        
        return True
    
    def test_bim_validation(self):
        """Test: Validazioni BIM."""
        print("\n🧪 Test: Validazioni BIM")
        
        # Test formato non supportato
        test_file_path = self.create_test_bim_file("txt")
        
        try:
            with open(test_file_path, 'rb') as f:
                files = {'file': ('test_model.txt', f, 'text/plain')}
                data = {'name': 'Test Invalid Format'}
                
                response = self.session.post(
                    f"{API_BASE}/bim/upload",
                    files=files,
                    data=data
                )
            
            os.unlink(test_file_path)
            
            if response.status_code == 400:
                print("✅ Validazione formato: rifiutato correttamente")
                return True
            else:
                print(f"❌ Validazione formato: accettato erroneamente ({response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ Errore validazione: {e}")
            os.unlink(test_file_path)
            return False
    
    def run_all_tests(self):
        """Esegue tutti i test BIM."""
        print("🚀 Avvio test API BIM per Eterna-Home")
        print("=" * 50)
        
        # Login
        if not self.login():
            return False
        
        # Ottieni dati di test
        self.get_test_data()
        
        # Esegui test
        tests = [
            ("Upload modello BIM", self.test_upload_bim_model),
            ("Lista modelli BIM", self.test_get_bim_models),
            ("Modello BIM specifico", self.test_get_bim_model_by_id),
            ("Formati BIM supportati", self.test_bim_formats),
            ("Validazioni BIM", self.test_bim_validation),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"❌ Test '{test_name}' fallito")
            except Exception as e:
                print(f"❌ Test '{test_name}' fallito con errore: {e}")
        
        # Risultati
        print("\n" + "=" * 50)
        print(f"📊 RISULTATI TEST: {passed}/{total} test passati")
        
        if passed == total:
            print("🎉 Tutti i test BIM sono passati!")
        else:
            print(f"⚠️  {total - passed} test falliti")
        
        return passed == total

if __name__ == "__main__":
    tester = BIMAPITester()
    success = tester.run_all_tests()
    
    if not success:
        print("\n💡 Suggerimenti:")
        print("1. Assicurati che il server sia in esecuzione su localhost:8000")
        print("2. Verifica che le credenziali di test siano corrette")
        print("3. Controlla che MinIO sia configurato correttamente")
        print("4. Verifica che ci siano case nel database")
    
    exit(0 if success else 1) 