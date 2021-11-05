import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { COMPONENTS, ManageUsersRoutingModule } from '@/manage-users/manage-users.routing.module'
import { DxDataGridModule, DxSpeedDialActionModule } from 'devextreme-angular'


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
