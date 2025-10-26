# Em config/settings.py (ARQUIVO PRONTO PARA O DEPLOY - VERSÃO CORRIGIDA)

from pathlib import Path
import os               # <--- MUDANÇA (Para ler variáveis de ambiente)
import dj_database_url  # <--- MUDANÇA (Para ler a URL do banco de dados)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ====================================================================
# MUDANÇAS PARA O DEPLOY (RENDER)
# ====================================================================

# 'RENDER' é uma variável que o site do Render cria.
# Se ela existir, DEBUG = False. Se não (no seu PC), DEBUG = True.
DEBUG = 'RENDER' not in os.environ

# Chave secreta: usa a do Render, ou a insegura se estiver no seu PC
if DEBUG:
    SECRET_KEY = 'django-insecure-wud%)#y0$$w6c5edhf+qdsoo$wt=*)j#5vh$+81w@r+im)*n85'
else:
    # Esta é a variável que vamos criar no Render
    SECRET_KEY = os.environ.get('SECRET_KEY')

# ====================================================================
# CORREÇÃO DO ALLOWED_HOSTS (PARA EVITAR O ERRO 'DisallowedHost')
# ====================================================================
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    # Se estiver no Render, pega o nome do host da variável de ambiente
    ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
else:
    # Senão (no seu PC), aceita apenas o IP local
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# ====================================================================


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # <--- MUDANÇA (Whitenoise)
    'django.contrib.staticfiles',
    
    # Nossos apps
    'usuarios',
    'apostas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- MUDANÇA (Whitenoise)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database (AGORA LÊ A URL DO RENDER)
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        # Se não achar a URL do Render, usa o sqlite (para o seu PC)
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Pasta onde o SEU style.css está (para o seu PC)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Pasta onde o Render vai JUNTAR todos os arquivos CSS (para a internet)
STATIC_ROOT = BASE_DIR / 'staticfiles' # <--- MUDANÇA (Obrigatório)

# O "entregador" de CSS (Whitenoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # <--- MUDANÇA

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Diz ao Django para usar nosso modelo customizado de usuário
AUTH_USER_MODEL = 'usuarios.UsuarioCustomizado'

LOGIN_REDIRECT_URL = 'home' # Para onde vai depois do LOGIN
LOGOUT_REDIRECT_URL = 'login' # Para onde vai depois do LOGOUT