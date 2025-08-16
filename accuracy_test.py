#!/usr/bin/env python3
"""
Comprehensive Accuracy Test for Fake News Detection System
Tests around 100 cases with known expected outcomes
"""

import requests
import json
import time
import statistics
from datetime import datetime
from typing import Dict, List, Tuple

class AccuracyTester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.results = []
        self.test_cases = self._generate_test_cases()
        
    def _generate_test_cases(self) -> List[Dict]:
        """Generate comprehensive test cases"""
        
        # Fake News Test Cases (50 cases)
        fake_news_cases = [
            # Sensationalist headlines
            {"text": "BREAKING: ALIENS CAUSING WEATHER CHANGES! Government hiding the truth!", "expected": "fake", "category": "conspiracy"},
            {"text": "SHOCKING: You won't BELIEVE what they found in the water supply!", "expected": "fake", "category": "clickbait"},
            {"text": "VIRAL: This one simple trick will save you from all disasters!", "expected": "fake", "category": "clickbait"},
            {"text": "URGENT: Share this NOW before they take it down!", "expected": "fake", "category": "viral"},
            {"text": "INCREDIBLE: Scientists discover secret weather control device!", "expected": "fake", "category": "conspiracy"},
            
            # Conspiracy theories
            {"text": "The government is hiding the real cause of climate change!", "expected": "fake", "category": "conspiracy"},
            {"text": "Chemtrails are poisoning our atmosphere!", "expected": "fake", "category": "conspiracy"},
            {"text": "Deep state controlling weather patterns!", "expected": "fake", "category": "conspiracy"},
            {"text": "They don't want you to know about HAARP!", "expected": "fake", "category": "conspiracy"},
            {"text": "Illuminati controlling natural disasters!", "expected": "fake", "category": "conspiracy"},
            
            # Excessive punctuation and caps
            {"text": "FIRE!!! WILDFIRE!!! EVERYONE MUST SHARE!!!", "expected": "fake", "category": "sensationalist"},
            {"text": "FLOOD ALERT!!! WATER RISING!!! HELP NEEDED!!!", "expected": "fake", "category": "sensationalist"},
            {"text": "HURRICANE COMING!!! STORM SURGE!!! EVACUATE NOW!!!", "expected": "fake", "category": "sensationalist"},
            {"text": "EARTHQUAKE!!! BUILDINGS SHAKING!!! PANIC!!!", "expected": "fake", "category": "sensationalist"},
            {"text": "DISASTER!!! CATASTROPHE!!! EMERGENCY!!!", "expected": "fake", "category": "sensationalist"},
            
            # Vague and unverifiable
            {"text": "Somewhere in the country, a major disaster is happening", "expected": "fake", "category": "vague"},
            {"text": "They say there's a huge fire burning", "expected": "fake", "category": "vague"},
            {"text": "Rumors of flooding in an unknown location", "expected": "fake", "category": "vague"},
            {"text": "Anonymous sources report earthquake damage", "expected": "fake", "category": "vague"},
            {"text": "Unconfirmed reports of hurricane damage", "expected": "fake", "category": "vague"},
            
            # Misinformation patterns
            {"text": "Fake news: Climate change is a hoax!", "expected": "fake", "category": "misinformation"},
            {"text": "Don't believe the mainstream media about disasters!", "expected": "fake", "category": "misinformation"},
            {"text": "Alternative facts about weather patterns", "expected": "fake", "category": "misinformation"},
            {"text": "The truth about natural disasters they don't tell you", "expected": "fake", "category": "misinformation"},
            {"text": "Real news: Everything you know about weather is wrong", "expected": "fake", "category": "misinformation"},
            
            # More fake cases
            {"text": "WAKE UP SHEEPLE! Weather control is real!", "expected": "fake", "category": "conspiracy"},
            {"text": "SHARE THIS: Secret weather modification program exposed!", "expected": "fake", "category": "conspiracy"},
            {"text": "AMAZING: One weird trick prevents all disasters!", "expected": "fake", "category": "clickbait"},
            {"text": "UNBELIEVABLE: What they found will shock you!", "expected": "fake", "category": "clickbait"},
            {"text": "MUST SEE: The truth about weather manipulation!", "expected": "fake", "category": "conspiracy"},
            
            # Additional fake cases to reach 50
            {"text": "BREAKING NEWS: Aliens controlling our weather!", "expected": "fake", "category": "conspiracy"},
            {"text": "SHOCKING DISCOVERY: Government hiding weather secrets!", "expected": "fake", "category": "conspiracy"},
            {"text": "VIRAL VIDEO: This will change everything you know!", "expected": "fake", "category": "clickbait"},
            {"text": "URGENT MESSAGE: Share before it gets deleted!", "expected": "fake", "category": "viral"},
            {"text": "INCREDIBLE FIND: Scientists baffled by weather patterns!", "expected": "fake", "category": "conspiracy"},
            {"text": "HIDDEN TRUTH: What they don't want you to know!", "expected": "fake", "category": "conspiracy"},
            {"text": "REAL STORY: Mainstream media won't report this!", "expected": "fake", "category": "misinformation"},
            {"text": "SECRET INFO: Weather control technology revealed!", "expected": "fake", "category": "conspiracy"},
            {"text": "AMAZING TRUTH: Natural disasters are man-made!", "expected": "fake", "category": "conspiracy"},
            {"text": "SHOCKING REALITY: Climate change is a scam!", "expected": "fake", "category": "misinformation"},
            {"text": "BREAKING: You won't believe what they found!", "expected": "fake", "category": "clickbait"},
            {"text": "URGENT: This information will be removed soon!", "expected": "fake", "category": "viral"},
            {"text": "INCREDIBLE: The real cause of weather changes!", "expected": "fake", "category": "conspiracy"},
            {"text": "MUST SHARE: The truth about natural disasters!", "expected": "fake", "category": "conspiracy"},
            {"text": "HIDDEN FACTS: What scientists won't tell you!", "expected": "fake", "category": "misinformation"},
            {"text": "REAL NEWS: Everything you know is wrong!", "expected": "fake", "category": "misinformation"},
            {"text": "SECRET REPORT: Weather manipulation exposed!", "expected": "fake", "category": "conspiracy"},
            {"text": "AMAZING DISCOVERY: The truth about climate!", "expected": "fake", "category": "conspiracy"},
            {"text": "SHOCKING TRUTH: Natural disasters are fake!", "expected": "fake", "category": "misinformation"},
            {"text": "BREAKING: This will change everything!", "expected": "fake", "category": "clickbait"},
            {"text": "URGENT: Share this important information!", "expected": "fake", "category": "viral"},
            {"text": "INCREDIBLE: The real story behind weather!", "expected": "fake", "category": "conspiracy"},
            {"text": "MUST READ: What they're hiding from you!", "expected": "fake", "category": "conspiracy"},
            {"text": "HIDDEN TRUTH: The real cause of disasters!", "expected": "fake", "category": "conspiracy"},
            {"text": "REAL FACTS: What the media won't tell you!", "expected": "fake", "category": "misinformation"},
            {"text": "SECRET INFO: Weather control revealed!", "expected": "fake", "category": "conspiracy"},
            {"text": "AMAZING TRUTH: Natural disasters are fake!", "expected": "fake", "category": "misinformation"},
            {"text": "SHOCKING: The real story about weather!", "expected": "fake", "category": "conspiracy"},
            {"text": "BREAKING: This information is being suppressed!", "expected": "fake", "category": "viral"},
            {"text": "URGENT: The truth they don't want you to know!", "expected": "fake", "category": "conspiracy"},
            {"text": "INCREDIBLE: Real cause of climate change!", "expected": "fake", "category": "conspiracy"},
            {"text": "MUST SHARE: The hidden truth about weather!", "expected": "fake", "category": "conspiracy"},
            {"text": "HIDDEN FACTS: What they're really doing!", "expected": "fake", "category": "conspiracy"},
            {"text": "REAL NEWS: The truth about natural disasters!", "expected": "fake", "category": "misinformation"},
            {"text": "SECRET REPORT: Weather manipulation truth!", "expected": "fake", "category": "conspiracy"},
            {"text": "AMAZING: The real story they're hiding!", "expected": "fake", "category": "conspiracy"},
            {"text": "SHOCKING: Natural disasters are man-made!", "expected": "fake", "category": "conspiracy"},
            {"text": "BREAKING: This will shock everyone!", "expected": "fake", "category": "clickbait"},
            {"text": "URGENT: The information they're suppressing!", "expected": "fake", "category": "viral"},
            {"text": "INCREDIBLE: The truth about weather control!", "expected": "fake", "category": "conspiracy"},
            {"text": "MUST READ: What they don't want you to know!", "expected": "fake", "category": "conspiracy"},
        ]
        
        # Real Disaster Test Cases (50 cases)
        real_disaster_cases = [
            # Wildfire cases
            {"text": "Firefighters responding to wildfire in northern California. Evacuation orders issued for residents in affected areas.", "expected": "real", "category": "wildfire"},
            {"text": "Wildfire spreading rapidly in forest area. Multiple fire departments on scene.", "expected": "real", "category": "wildfire"},
            {"text": "Smoke visible from wildfire in mountain region. Air quality warnings issued.", "expected": "real", "category": "wildfire"},
            {"text": "Fire crews battling blaze in rural area. Wind conditions making containment difficult.", "expected": "real", "category": "wildfire"},
            {"text": "Wildfire evacuation center opened at local high school. Red Cross providing assistance.", "expected": "real", "category": "wildfire"},
            
            # Flood cases
            {"text": "Heavy rainfall causing flooding in downtown area. Water levels rising rapidly.", "expected": "real", "category": "flood"},
            {"text": "Flash flood warning issued for coastal region. Emergency services on scene.", "expected": "real", "category": "flood"},
            {"text": "River overflow causing flooding in residential areas. Evacuation orders in place.", "expected": "real", "category": "flood"},
            {"text": "Heavy storms causing street flooding. Traffic delays expected.", "expected": "real", "category": "flood"},
            {"text": "Flood damage reported in several neighborhoods. Cleanup efforts underway.", "expected": "real", "category": "flood"},
            
            # Hurricane cases
            {"text": "Hurricane approaching coastal region. Mandatory evacuation orders issued.", "expected": "real", "category": "hurricane"},
            {"text": "Tropical storm strengthening into hurricane. Emergency preparations advised.", "expected": "real", "category": "hurricane"},
            {"text": "Hurricane making landfall. High winds and heavy rain expected.", "expected": "real", "category": "hurricane"},
            {"text": "Storm surge warning issued for coastal areas. Residents urged to evacuate.", "expected": "real", "category": "hurricane"},
            {"text": "Hurricane damage assessment underway. Power outages reported.", "expected": "real", "category": "hurricane"},
            
            # Earthquake cases
            {"text": "Earthquake measuring 6.2 magnitude reported in region. Building damage reported.", "expected": "real", "category": "earthquake"},
            {"text": "Seismic activity detected. Aftershocks expected in coming hours.", "expected": "real", "category": "earthquake"},
            {"text": "Earthquake causing structural damage to buildings. Emergency response teams deployed.", "expected": "real", "category": "earthquake"},
            {"text": "Tremor felt across metropolitan area. No major damage reported.", "expected": "real", "category": "earthquake"},
            {"text": "Earthquake epicenter located near fault line. Tsunami warning issued.", "expected": "real", "category": "earthquake"},
            
            # More real cases
            {"text": "Emergency services responding to natural disaster. Multiple agencies coordinating response.", "expected": "real", "category": "general"},
            {"text": "Disaster relief efforts underway. Volunteers needed for cleanup operations.", "expected": "real", "category": "general"},
            {"text": "Weather service issuing severe weather warnings. Public advised to take precautions.", "expected": "real", "category": "general"},
            {"text": "Emergency shelters opened for disaster victims. Food and medical assistance available.", "expected": "real", "category": "general"},
            {"text": "Damage assessment teams evaluating disaster impact. Recovery timeline estimated.", "expected": "real", "category": "general"},
            
            # Additional real cases to reach 50
            {"text": "Fire department responding to structure fire. Smoke visible from several blocks away.", "expected": "real", "category": "fire"},
            {"text": "Heavy snow causing road closures. Travel advisories in effect.", "expected": "real", "category": "winter"},
            {"text": "Tornado warning issued for county. Residents advised to seek shelter.", "expected": "real", "category": "tornado"},
            {"text": "Landslide reported on mountain road. Highway closed for safety.", "expected": "real", "category": "landslide"},
            {"text": "Drought conditions affecting agricultural areas. Water restrictions implemented.", "expected": "real", "category": "drought"},
            {"text": "Heat wave causing health concerns. Cooling centers opened.", "expected": "real", "category": "heat"},
            {"text": "Avalanche warning issued for ski resort. Mountain access restricted.", "expected": "real", "category": "avalanche"},
            {"text": "Volcanic activity increasing. Evacuation orders for nearby communities.", "expected": "real", "category": "volcano"},
            {"text": "Tsunami warning issued for coastal areas. Residents urged to move to higher ground.", "expected": "real", "category": "tsunami"},
            {"text": "Blizzard conditions causing travel disruptions. Emergency services on standby.", "expected": "real", "category": "winter"},
            {"text": "Lightning storm causing power outages. Utility crews working to restore service.", "expected": "real", "category": "storm"},
            {"text": "Hail storm damaging vehicles and property. Insurance claims expected to increase.", "expected": "real", "category": "storm"},
            {"text": "Dust storm reducing visibility on highways. Travel warnings issued.", "expected": "real", "category": "storm"},
            {"text": "Ice storm causing dangerous road conditions. School closures announced.", "expected": "real", "category": "winter"},
            {"text": "Wind storm causing tree damage. Debris removal operations planned.", "expected": "real", "category": "storm"},
            {"text": "Thunderstorm causing flash flooding. Emergency response teams activated.", "expected": "real", "category": "storm"},
            {"text": "Fog reducing visibility on major highways. Traffic delays reported.", "expected": "real", "category": "weather"},
            {"text": "High winds causing power line damage. Electrical service interruptions expected.", "expected": "real", "category": "storm"},
            {"text": "Heavy rain causing mudslides. Road closures in affected areas.", "expected": "real", "category": "landslide"},
            {"text": "Snow storm causing school closures. Emergency services on alert.", "expected": "real", "category": "winter"},
            {"text": "Freezing rain creating hazardous conditions. Travel advisories in effect.", "expected": "real", "category": "winter"},
            {"text": "Severe thunderstorm warning issued. Residents advised to stay indoors.", "expected": "real", "category": "storm"},
            {"text": "Flood watch in effect for river basin. Water levels being monitored.", "expected": "real", "category": "flood"},
            {"text": "Fire danger high due to dry conditions. Burn bans implemented.", "expected": "real", "category": "fire"},
            {"text": "Tropical depression forming in Atlantic. Weather service monitoring.", "expected": "real", "category": "hurricane"},
            {"text": "Seismic monitoring equipment detecting activity. Geologists analyzing data.", "expected": "real", "category": "earthquake"},
            {"text": "Emergency management coordinating disaster response. Resources being deployed.", "expected": "real", "category": "general"},
            {"text": "Weather radar showing severe storm development. Warnings being issued.", "expected": "real", "category": "storm"},
            {"text": "Disaster declaration issued for affected region. Federal assistance requested.", "expected": "real", "category": "general"},
            {"text": "Emergency operations center activated. Response teams on standby.", "expected": "real", "category": "general"},
            {"text": "Weather service updating forecast models. Public advisories being prepared.", "expected": "real", "category": "weather"},
            {"text": "Emergency communications system tested. Response protocols reviewed.", "expected": "real", "category": "general"},
            {"text": "Disaster preparedness training conducted. Emergency procedures practiced.", "expected": "real", "category": "general"},
            {"text": "Weather monitoring stations reporting data. Conditions being tracked.", "expected": "real", "category": "weather"},
            {"text": "Emergency response vehicles deployed. Personnel on scene.", "expected": "real", "category": "general"},
            {"text": "Disaster assessment teams mobilized. Damage surveys beginning.", "expected": "real", "category": "general"},
            {"text": "Weather warning system activated. Public notifications sent.", "expected": "real", "category": "weather"},
            {"text": "Emergency shelter locations announced. Evacuation routes mapped.", "expected": "real", "category": "general"},
            {"text": "Disaster recovery planning initiated. Long-term assistance considered.", "expected": "real", "category": "general"},
            {"text": "Weather service coordinating with emergency managers. Response plans updated.", "expected": "real", "category": "weather"},
            {"text": "Emergency medical services on alert. Hospital capacity being monitored.", "expected": "real", "category": "general"},
            {"text": "Disaster relief organizations mobilizing. Volunteer coordination underway.", "expected": "real", "category": "general"},
            {"text": "Weather conditions being monitored continuously. Updates provided regularly.", "expected": "real", "category": "weather"},
            {"text": "Emergency response protocols being followed. Safety measures implemented.", "expected": "real", "category": "general"},
            {"text": "Disaster impact assessment continuing. Recovery efforts planned.", "expected": "real", "category": "general"},
            {"text": "Weather service providing regular updates. Public information disseminated.", "expected": "real", "category": "weather"},
            {"text": "Emergency management coordinating response efforts. Resources allocated.", "expected": "real", "category": "general"},
            {"text": "Disaster response teams working efficiently. Coordination improving.", "expected": "real", "category": "general"},
            {"text": "Weather monitoring continuing. Conditions being tracked closely.", "expected": "real", "category": "weather"},
            {"text": "Emergency services responding appropriately. Public safety maintained.", "expected": "real", "category": "general"},
            {"text": "Disaster recovery progressing. Community resilience demonstrated.", "expected": "real", "category": "general"},
            {"text": "Weather service maintaining vigilance. Public safety prioritized.", "expected": "real", "category": "weather"},
            {"text": "Emergency response effective. Coordination successful.", "expected": "real", "category": "general"},
            {"text": "Disaster management professional. Standards maintained.", "expected": "real", "category": "general"},
            {"text": "Weather monitoring comprehensive. Data collection ongoing.", "expected": "real", "category": "weather"},
            {"text": "Emergency services professional. Response coordinated.", "expected": "real", "category": "general"},
            {"text": "Disaster recovery systematic. Progress documented.", "expected": "real", "category": "general"},
            {"text": "Weather service reliable. Information accurate.", "expected": "real", "category": "weather"},
            {"text": "Emergency management effective. Response timely.", "expected": "real", "category": "general"},
            {"text": "Disaster response coordinated. Resources utilized.", "expected": "real", "category": "general"},
            {"text": "Weather monitoring continuous. Updates regular.", "expected": "real", "category": "weather"},
            {"text": "Emergency services available. Response ready.", "expected": "real", "category": "general"},
            {"text": "Disaster recovery planned. Assistance available.", "expected": "real", "category": "general"},
            {"text": "Weather service operational. Monitoring active.", "expected": "real", "category": "weather"},
            {"text": "Emergency management prepared. Response capable.", "expected": "real", "category": "general"},
            {"text": "Disaster response organized. Coordination effective.", "expected": "real", "category": "general"},
            {"text": "Weather monitoring ongoing. Conditions tracked.", "expected": "real", "category": "weather"},
            {"text": "Emergency services responsive. Help available.", "expected": "real", "category": "general"},
            {"text": "Disaster recovery supported. Community assisted.", "expected": "real", "category": "general"},
        ]
        
        return fake_news_cases + real_disaster_cases
    
    def test_single_case(self, test_case: Dict) -> Dict:
        """Test a single case and return results"""
        try:
            response = requests.post(
                f"{self.base_url}/api/analyze",
                json={'text': test_case['text']},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get('multimodal_analysis', {}).get('prediction', 'unknown')
                confidence = result.get('multimodal_analysis', {}).get('confidence', 0)
                
                # Determine if prediction is correct
                is_correct = test_case['expected'] in prediction.lower()
                
                return {
                    'text': test_case['text'][:50] + "...",
                    'expected': test_case['expected'],
                    'predicted': prediction,
                    'confidence': confidence,
                    'category': test_case['category'],
                    'correct': is_correct,
                    'status': 'success'
                }
            else:
                return {
                    'text': test_case['text'][:50] + "...",
                    'expected': test_case['expected'],
                    'predicted': 'error',
                    'confidence': 0,
                    'category': test_case['category'],
                    'correct': False,
                    'status': f'error_{response.status_code}'
                }
                
        except Exception as e:
            return {
                'text': test_case['text'][:50] + "...",
                'expected': test_case['expected'],
                'predicted': 'exception',
                'confidence': 0,
                'category': test_case['category'],
                'correct': False,
                'status': f'exception_{str(e)[:50]}'
            }
    
    def run_accuracy_test(self) -> Dict:
        """Run the complete accuracy test"""
        print("🚀 Starting Comprehensive Accuracy Test")
        print("=" * 60)
        print(f"Total test cases: {len(self.test_cases)}")
        print(f"Fake news cases: {len([c for c in self.test_cases if c['expected'] == 'fake'])}")
        print(f"Real disaster cases: {len([c for c in self.test_cases if c['expected'] == 'real'])}")
        print("=" * 60)
        
        start_time = time.time()
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"Testing case {i}/{len(self.test_cases)}: {test_case['category']} - {test_case['expected']}")
            
            result = self.test_single_case(test_case)
            self.results.append(result)
            
            # Progress indicator
            if i % 10 == 0:
                correct_so_far = sum(1 for r in self.results if r['correct'])
                accuracy_so_far = (correct_so_far / i) * 100
                print(f"   Progress: {i}/{len(self.test_cases)} - Accuracy: {accuracy_so_far:.1f}%")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.1)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return self._calculate_metrics(total_time)
    
    def _calculate_metrics(self, total_time: float) -> Dict:
        """Calculate comprehensive accuracy metrics"""
        
        # Overall metrics
        total_tests = len(self.results)
        correct_predictions = sum(1 for r in self.results if r['correct'])
        overall_accuracy = (correct_predictions / total_tests) * 100
        
        # Separate metrics for fake and real
        fake_results = [r for r in self.results if r['expected'] == 'fake']
        real_results = [r for r in self.results if r['expected'] == 'real']
        
        fake_correct = sum(1 for r in fake_results if r['correct'])
        real_correct = sum(1 for r in real_results if r['correct'])
        
        fake_accuracy = (fake_correct / len(fake_results)) * 100 if fake_results else 0
        real_accuracy = (real_correct / len(real_results)) * 100 if real_results else 0
        
        # Category-wise accuracy
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'correct': 0}
            categories[cat]['total'] += 1
            if result['correct']:
                categories[cat]['correct'] += 1
        
        category_accuracy = {}
        for cat, stats in categories.items():
            category_accuracy[cat] = (stats['correct'] / stats['total']) * 100
        
        # Confidence analysis
        confidences = [r['confidence'] for r in self.results if r['confidence'] > 0]
        avg_confidence = statistics.mean(confidences) if confidences else 0
        
        # Error analysis
        errors = [r for r in self.results if not r['correct']]
        error_types = {}
        for error in errors:
            error_type = f"{error['expected']}_classified_as_{error['predicted']}"
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'summary': {
                'total_tests': total_tests,
                'correct_predictions': correct_predictions,
                'overall_accuracy': overall_accuracy,
                'fake_accuracy': fake_accuracy,
                'real_accuracy': real_accuracy,
                'avg_confidence': avg_confidence,
                'total_time_seconds': total_time,
                'avg_time_per_test': total_time / total_tests
            },
            'category_accuracy': category_accuracy,
            'error_analysis': error_types,
            'detailed_results': self.results
        }
    
    def print_results(self, metrics: Dict):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE ACCURACY TEST RESULTS")
        print("=" * 60)
        
        summary = metrics['summary']
        print(f"\n🎯 OVERALL PERFORMANCE:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Correct Predictions: {summary['correct_predictions']}")
        print(f"   Overall Accuracy: {summary['overall_accuracy']:.2f}%")
        print(f"   Average Confidence: {summary['avg_confidence']:.3f}")
        print(f"   Total Time: {summary['total_time_seconds']:.2f} seconds")
        print(f"   Average Time per Test: {summary['avg_time_per_test']:.3f} seconds")
        
        print(f"\n📈 ACCURACY BREAKDOWN:")
        print(f"   Fake News Detection: {summary['fake_accuracy']:.2f}%")
        print(f"   Real Disaster Detection: {summary['real_accuracy']:.2f}%")
        
        print(f"\n🏷️  CATEGORY-WISE ACCURACY:")
        for category, accuracy in metrics['category_accuracy'].items():
            print(f"   {category}: {accuracy:.2f}%")
        
        print(f"\n❌ ERROR ANALYSIS:")
        for error_type, count in metrics['error_analysis'].items():
            print(f"   {error_type}: {count} cases")
        
        print(f"\n📋 DETAILED RESULTS:")
        print("   (First 10 results shown)")
        for i, result in enumerate(metrics['detailed_results'][:10]):
            status_icon = "✅" if result['correct'] else "❌"
            print(f"   {i+1}. {status_icon} Expected: {result['expected']}, Predicted: {result['predicted']}, Confidence: {result['confidence']:.3f}")
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"accuracy_test_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"\n💾 Results saved to: {filename}")

def main():
    """Main function to run the accuracy test"""
    tester = AccuracyTester()
    
    try:
        # Test backend connectivity first
        print("🔍 Testing backend connectivity...")
        response = requests.get("http://localhost:5000/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is accessible")
        else:
            print("❌ Backend health check failed")
            return
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        print("Please start the backend first: cd backend && python app.py")
        return
    
    # Run the accuracy test
    metrics = tester.run_accuracy_test()
    tester.print_results(metrics)

if __name__ == "__main__":
    main()
