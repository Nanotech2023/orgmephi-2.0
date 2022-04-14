import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { ManageUsersComponent } from '@/manage-users/containers/manage-users/manage-users.component'
import { AdminAuthGuardService } from '@/shared/admin.auth.guard.service'


export const COMPONENTS = [
    ManageUsersComponent
]


const routes: Routes =
    [
        {
            path: 'manage/users',
            component: ManageUsersComponent,
            canActivate: [ AdminAuthGuardService ]
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ManageUsersRoutingModule {}