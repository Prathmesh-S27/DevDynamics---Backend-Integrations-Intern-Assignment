<attachment id="file:alembic/script.py.mako">
--8<-- 
""" 
Revision ID: ${rev} 
Revises: ${down_revision} 
Create Date: ${create_date} 
""" 

from alembic import op 
import sqlalchemy as sa 

# revision identifiers, used by Alembic. 
revision = '${rev}' 
down_revision = '${down_revision}' 
branch_labels = None 
depends_on = None 

def upgrade(): 
    pass 

def downgrade(): 
    pass 
--8<-- 
</attachment>