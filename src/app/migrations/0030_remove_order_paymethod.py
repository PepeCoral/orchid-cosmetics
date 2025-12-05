from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_remove_order_paymethod_order_shipping_costs_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # Operaciones para el estado de Django (vacío si ya se eliminó)
            ],
            database_operations=[
                # Solo intentar eliminar si existe
                migrations.RunSQL(
                    sql="""
                    SELECT CASE 
                        WHEN COUNT(*) > 0 THEN 
                            'ALTER TABLE app_order DROP COLUMN payMethod'
                        ELSE 'SELECT 1'
                    END
                    FROM pragma_table_info('app_order')
                    WHERE name = 'payMethod';
                    """,
                    reverse_sql=migrations.RunSQL.noop
                ),
            ],
        ),
    ]