import { NgModule } from '@angular/core'
import { AdminComponent } from './containers/admin/admin.component'
import { ManageUsersComponent } from './components/manage-users/manage-users.component'
import { ManageOlympiadsComponent } from './components/manage-olympiads/manage-olympiads.component'
import { SharedModule } from '@/shared/shared.module'
import { AdminRoutingModule } from '@/admin/admin-routing.module'
import { AgGridModule } from 'ag-grid-angular'


const COMPONENTS = [
    ManageUsersComponent,
    ManageOlympiadsComponent,
    AdminComponent
]


@NgModule( {
    declarations: [
        COMPONENTS
    ],
    imports: [
        SharedModule,
        AgGridModule,
        AdminRoutingModule
    ],
    exports: [
        AdminRoutingModule
    ]
} )

export class AdminModule {}