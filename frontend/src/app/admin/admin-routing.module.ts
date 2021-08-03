import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { AdminComponent } from '@/admin/containers/admin/admin.component'
import { ManageOlympiadsComponent } from '@/admin/components/manage-olynpiads/manage-olympiads.component'
import { ManageUsersComponent } from '@/admin/components/manage-users/manage-users.component'


const routes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'admin', component: AdminComponent
            },
            {
                path: 'admin/olymp', component: ManageOlympiadsComponent
            },
            {
                path: 'admin/users', component: ManageUsersComponent
            }
        ]
    }
]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )

export class AdminRoutingModule {}