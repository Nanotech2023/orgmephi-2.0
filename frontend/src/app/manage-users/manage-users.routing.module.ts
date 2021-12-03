import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { ManageUsersComponent } from '@/manage-users/containers/manage-users/manage-users.component'


export const COMPONENTS = [
    ManageUsersComponent
]


const routes: Routes =
    [
        {
            path: 'manage/users', component: ManageUsersComponent
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ManageUsersRoutingModule {}