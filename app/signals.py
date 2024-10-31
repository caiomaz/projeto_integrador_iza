from django.db.models.signals import post_migrate, pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import (
    Categoria, Marca, Produto, Cliente, Venda, ItemVenda, Pagamento,
    EnderecoEntrega, Avaliacao, Comentario, Cupom, Carrinho, 
    ItemCarrinho, Desejo, ItemDesejo, Notificacao, Log
)
import inspect


#############################################################################################
# ARQUIVO DE SINAIS DA APLICAÇÃO (QUANDO DETERMINADO EVENTO OCORRE, UMA FUNÇÃO É EXECUTADA) #
#############################################################################################


# Cria objetos padrão caso não existam
@receiver(post_migrate)
def create_default_objects(sender, **kwargs):
    Categoria.create_default()
    Marca.create_default()
    Produto.create_default()
    Cliente.create_default()
    Venda.create_default()
    ItemVenda.create_default()
    Pagamento.create_default()
    EnderecoEntrega.create_default()
    Avaliacao.create_default()
    Comentario.create_default()
    Cupom.create_default()
    Carrinho.create_default()
    ItemCarrinho.create_default()
    Desejo.create_default()
    ItemDesejo.create_default()
    Notificacao.create_default()


# Cria um usuário padrão caso não exista
@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    if not User.objects.exists():
        User.objects.create_user(
            username='defaultuser',
            password='defaultpassword',
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )


# Lista de modelos para monitorar alterações
MONITORED_MODELS = [
    Categoria, Marca, Produto, Cliente, Venda, ItemVenda, Pagamento,
    EnderecoEntrega, Avaliacao, Comentario, Cupom, Carrinho, 
    ItemCarrinho, Desejo, ItemDesejo, Notificacao
]


# Função auxiliar para salvar logs
def save_log(instance, field, old_value, new_value, action, user):
    Log.objects.create(
        tabela=instance._meta.model_name,
        objeto=instance.pk,
        campo=field,
        valor_antigo=str(old_value),
        valor_novo=str(new_value),
        acao=action,
        usuario=user
    )


# Sinal para capturar alterações antes de salvar (pre-save)
@receiver(pre_save)
def track_changes(sender, instance, **kwargs):
    # Ignorar modelos que não estão monitorados
    if sender not in MONITORED_MODELS:
        return

    # Checa se a instância já existe no banco de dados (update)
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name)
            new_value = getattr(instance, field_name)

            # Se o valor mudou, armazena em cache para o sinal post_save
            if old_value != new_value:
                setattr(instance, f'_old_{field_name}', old_value)


# Sinal para capturar e salvar logs após salvar (post-save)
@receiver(post_save)
def log_changes(sender, instance, created, **kwargs):
    # Ignorar modelos que não estão monitorados
    if sender not in MONITORED_MODELS:
        return

    user = get_user_model().objects.filter(is_superuser=True).first()  # Usuário padrão, ajuste conforme necessário

    # Caso de criação (insert)
    if created:
        for field in instance._meta.fields:
            field_name = field.name
            new_value = getattr(instance, field_name)
            save_log(instance, field_name, None, new_value, "CREATE", user)
    else:
        # Caso de atualização (update)
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(instance, f'_old_{field_name}', None)
            new_value = getattr(instance, field_name)

            # Salva apenas os campos que foram alterados
            if old_value is not None and old_value != new_value:
                save_log(instance, field_name, old_value, new_value, "UPDATE", user)


# Sinal para capturar exclusões antes de deletar (pre-delete)
@receiver(pre_delete)
def log_deletions(sender, instance, **kwargs):
    # Ignorar modelos que não estão monitorados
    if sender not in MONITORED_MODELS:
        return

    user = get_user_model().objects.filter(is_superuser=True).first()  # Usuário padrão, ajuste conforme necessário

    # Caso de exclusão (delete)
    for field in instance._meta.fields:
        field_name = field.name
        old_value = getattr(instance, field_name)
        save_log(instance, field_name, old_value, None, "DELETE", user)
        