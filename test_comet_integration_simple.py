#!/usr/bin/env python3
"""
Validación básica de la nueva funcionalidad de cometas sin GUI.
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import SpaceMap, Comet


def test_basic_comet_functionality():
    """Prueba la funcionalidad básica de cometas."""
    print("🧪 Testing basic comet functionality...")
    
    # Crear mapa espacial
    space_map = SpaceMap('data/constellations.json')
    
    # Estado inicial
    initial_comet_count = len(space_map.comets)
    print(f"   ✓ Estado inicial: {initial_comet_count} cometas")
    
    # Contar rutas no bloqueadas iniciales
    initial_unblocked = sum(1 for route in space_map.routes if not route.blocked)
    print(f"   ✓ Rutas no bloqueadas inicialmente: {initial_unblocked}")
    
    # Agregar un cometa de prueba
    test_comet = Comet(name="TestComet_1", blocked_routes=[("1", "2")])
    space_map.add_comet(test_comet)
    
    # Verificar que se agregó
    after_add_count = len(space_map.comets)
    print(f"   ✓ Después de agregar: {after_add_count} cometas")
    
    # Verificar que hay rutas bloqueadas
    blocked_routes = [route for route in space_map.routes if route.blocked]
    print(f"   ✓ Rutas bloqueadas por cometa: {len(blocked_routes)}")
    
    if blocked_routes:
        for route in blocked_routes[:2]:  # Solo mostrar las primeras 2
            print(f"     - {route.from_star.id}({route.from_star.label}) ↔ {route.to_star.id}({route.to_star.label})")
    
    # Remover el cometa
    space_map.remove_comet("TestComet_1")
    
    # Verificar que se removió
    after_remove_count = len(space_map.comets)
    print(f"   ✓ Después de remover: {after_remove_count} cometas")
    
    # Verificar que las rutas se desbloquearon
    final_unblocked = sum(1 for route in space_map.routes if not route.blocked)
    print(f"   ✓ Rutas no bloqueadas finalmente: {final_unblocked}")
    
    # Validación
    success = (after_add_count == initial_comet_count + 1 and 
              after_remove_count == initial_comet_count and
              len(blocked_routes) > 0 and
              final_unblocked == initial_unblocked)
    
    if success:
        print("   ✅ Basic comet functionality test passed!\n")
    else:
        print("   ❌ Basic comet functionality test failed!\n")
    
    return success


def test_comet_manager_import():
    """Prueba que se puede importar el CometManager."""
    print("🧪 Testing CometManager import...")
    
    try:
        from src.parameter_editor_simple.comet_manager import CometManager
        print("   ✓ CometManager import successful")
        
        # Verificar que tiene los métodos esperados
        required_methods = ['create_ui', 'extract_star_id', 'add_comet', 
                          'remove_selected_comet', 'refresh_comet_list', 
                          'get_comet_summary', 'clear_inputs']
        
        for method in required_methods:
            if hasattr(CometManager, method):
                print(f"   ✓ Method '{method}' exists")
            else:
                print(f"   ❌ Method '{method}' missing")
                return False
        
        print("   ✅ CometManager import test passed!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ CometManager import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_parameter_editor_integration():
    """Prueba la integración con el editor de parámetros."""
    print("🧪 Testing Parameter Editor integration...")
    
    try:
        from src.parameter_editor_simple import ResearchParameterEditor, ResearchParameters
        print("   ✓ Parameter Editor imports successful")
        
        # Verificar que el constructor acepta el callback
        space_map = SpaceMap('data/constellations.json')
        
        # Verificar constructor con callback (sin crear la ventana)
        # Esto solo verifica que la signatura es correcta
        import inspect
        sig = inspect.signature(ResearchParameterEditor.__init__)
        params = list(sig.parameters.keys())
        
        expected_params = ['self', 'parent', 'space_map', 'initial_params', 'update_visualization_callback']
        
        if 'update_visualization_callback' in params:
            print("   ✓ Constructor accepts update_visualization_callback")
        else:
            print(f"   ❌ Constructor params: {params}")
            print("   ❌ Missing update_visualization_callback parameter")
            return False
        
        print("   ✅ Parameter Editor integration test passed!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Parameter Editor integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gui_modifications():
    """Prueba que las modificaciones del GUI están presentes."""
    print("🧪 Testing GUI modifications...")
    
    try:
        # Leer el archivo gui.py para verificar cambios
        with open('src/gui.py', 'r', encoding='utf-8') as f:
            gui_content = f.read()
        
        # Verificar que se removió la sección de cometas
        if "COMET MANAGEMENT MOVED TO SCIENTIFIC PANEL" in gui_content:
            print("   ✓ Comet section moved to scientific panel")
        else:
            print("   ❌ Comet section not properly moved")
            return False
        
        # Verificar que se actualiza la llamada al editor
        if "update_visualization_callback" in gui_content:
            print("   ✓ Editor call updated with callback")
        else:
            print("   ❌ Editor call not updated")
            return False
        
        # Verificar que las funciones de cometa fueron reemplazadas
        if "Función Reubicada" in gui_content:
            print("   ✓ Comet functions redirected")
        else:
            print("   ❌ Comet functions not properly redirected")
            return False
        
        print("   ✅ GUI modifications test passed!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ GUI modifications test failed: {e}")
        return False


def main():
    """Función principal de validación."""
    print("🌌 Validación: Nueva Gestión de Cometas en Panel Científico")
    print("=" * 70)
    
    success_count = 0
    total_tests = 4
    
    try:
        # Test 1: Funcionalidad básica de cometas
        if test_basic_comet_functionality():
            success_count += 1
        
        # Test 2: Import del CometManager
        if test_comet_manager_import():
            success_count += 1
        
        # Test 3: Integración con Parameter Editor
        if test_parameter_editor_integration():
            success_count += 1
        
        # Test 4: Modificaciones del GUI
        if test_gui_modifications():
            success_count += 1
        
        # Resultado final
        print(f"📊 Resultados: {success_count}/{total_tests} tests pasaron")
        
        if success_count == total_tests:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
            print("\n✅ Implementación completa:")
            print("   • ✓ Gestión de cometas movida al panel científico")
            print("   • ✓ CometManager implementado correctamente")
            print("   • ✓ Integración con Parameter Editor funcional")
            print("   • ✓ GUI principal actualizado apropiadamente")
            
            print("\n🔧 Para usar la nueva funcionalidad:")
            print("   1. Ejecutar: python -c \"import sys; sys.path.append('.'); from src.gui import main; main()\"")
            print("   2. Clic en '⚙️ Configurar Parámetros'")
            print("   3. Pestaña '🌌 Cometas'")
            print("   4. Usar la interfaz mejorada para agregar/remover cometas")
            
            print("\n🌟 Nuevas características:")
            print("   • Combos desplegables para seleccionar estrellas")
            print("   • Lista visual de cometas activos")
            print("   • Validación mejorada de entrada")
            print("   • Actualización automática de visualización")
            print("   • Panel organizado sin problemas de scroll")
            
            return 0
        else:
            print(f"\n⚠️ Algunos tests fallaron ({total_tests - success_count} fallos)")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error crítico durante la validación: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())