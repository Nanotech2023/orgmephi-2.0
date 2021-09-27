import { NgModule } from '@angular/core'
import { ManageUsersComponent } from '@/manage-users/containers/manage-users/manage-users.component'
import { AddUserModalComponent } from '@/manage-users/components/add-user-modal/add-user-modal.component'
import { EditUserModalComponent } from '@/manage-users/components/edit-user-modal/edit-user-modal.component'
import { SharedModule } from '@/shared/shared.module'
import { AgGridModule } from 'ag-grid-angular'
import { ManageUsersRoutingModule } from '@/manage-users/manage-users.routing.module'


const COMPONENTS = [
    ManageUsersComponent,
    AddUserModalComponent,
    EditUserModalComponent
]


@NgModule( {
    declarations: [
        COMPONENTS
    ],
    imports: [
        SharedModule,
        AgGridModule,
        ManageUsersRoutingModule
    ],
    exports: [
        ManageUsersRoutingModule
    ]
} )
export class ManageUsersModule {}
