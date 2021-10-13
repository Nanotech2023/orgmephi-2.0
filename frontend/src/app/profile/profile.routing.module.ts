import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { ProfileViewComponent } from '@/profile/containers/profile-view/profile-view.component'
import { AuthGuardService } from '@/shared/auth.guard.service'


const routes: Routes =
    [
        {
            path: 'profile', component: ProfileViewComponent, canActivate: [ AuthGuardService ]
        },
        // {
        //     path: 'profile/edit', component: ProfileEditComponent, canActivate: [ AuthGuardService ]
        // }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ProfileRoutingModule {}