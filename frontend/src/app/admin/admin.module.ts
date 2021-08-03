import { NgModule } from '@angular/core'
import { AdminComponent } from './containers/admin/admin.component'
import { ManageUsersComponent } from './components/manage-users/manage-users.component'
import { ManageOlympiadsComponent } from './components/manage-olynpiads/manage-olympiads.component'
import { SharedModule } from '@/shared/shared.module'
import { AdminRoutingModule } from '@/admin/admin-routing.module'
import { AgGridModule } from 'ag-grid-angular'


const COMPONENTS = [
    ManageUsersComponent, ManageOlympiadsComponent, AdminComponent
]


@NgModule( {
    declarations: [
        COMPONENTS
    ],
    imports: [
        AdminRoutingModule,
        SharedModule,
        AgGridModule
    ],
    exports: [
        AdminRoutingModule
    ]
} )

export class AdminModule {}