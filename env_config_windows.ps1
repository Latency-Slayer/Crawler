echo "Configurando seu ambiente..."

echo "Verificando dependencias..."


try {
    $pythonVersion = python --version 2>$null  # Tenta executar o Python
    if ($?) {
        echo "Python encontrado: $pythonVersion"
    } else {
        throw "Python não está instalado. Instale o python."


    }
} catch {
    echo "Erro: Python não está instalado ou não está no PATH."
    exit 1  
}


