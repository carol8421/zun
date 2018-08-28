# Copyright 2017 ARM Holdings
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""add auto heal to container

Revision ID: 372433c0afd2
Revises: d0c606fdec3c
Create Date: 2018-03-12 14:18:44.545951

"""

# revision identifiers, used by Alembic.
revision = '372433c0afd2'
down_revision = 'd0c606fdec3c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('container', schema=None) as batch_op:
        batch_op.add_column(sa.Column('auto_heal',
                                      sa.Boolean(), nullable=True))
    # ### end Alembic commands ###