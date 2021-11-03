import { NgModule } from '@angular/core'
import { ManageUsersComponent } from '@/manage-users/containers/manage-users/manage-users.component'
import { SharedModule } from '@/shared/shared.module'
import { ManageUsersRoutingModule } from '@/manage-users/manage-users.routing.module'
import { DxDataGridModule, DxSpeedDialActionModule } from 'devextreme-angular'


const COMPONENTS = [
    ManageUsersComponent
]


@NgModule( {
    declarations: [
        COMPONENTS
    ],
    imports: [
        SharedModule,
        DxDataGridModule,
        DxSpeedDialActionModule,
        ManageUsersRoutingModule
    ]
} )
export class ManageUsersModule {}
