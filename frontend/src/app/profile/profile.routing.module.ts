import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { AuthGuardService } from '@/shared/auth.guard.service'
import { ProfileEditComponent } from '@/profile/containers/profile-edit/profile-edit.component'
import {
    ProfileEditUserinfoComponent
} from '@/profile/containers/profile-edit-userinfo/profile-edit-userinfo.component'
import { ProfileEditSchoolComponent } from '@/profile/containers/profile-edit-school/profile-edit-school.component'
import {
    ProfileEditPasswordComponent
} from '@/profile/containers/profile-edit-password/profile-edit-password.component'


const routes: Routes =
    [
        {
            path: 'profile', component: ProfileEditComponent, canActivate: [ AuthGuardService ],
            children: [
                {
                    path: '', pathMatch: 'full', redirectTo: 'userinfo'
                },
                {
                    path: 'userinfo',
                    component: ProfileEditUserinfoComponent
                },
                {
                    path: 'schoolinfo',
                    component: ProfileEditSchoolComponent
                },
                {
                    path: 'password',
                    component: ProfileEditPasswordComponent
                }
            ]
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ProfileRoutingModule {}