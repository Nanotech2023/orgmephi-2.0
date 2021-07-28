import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { HomeComponent } from '@/users/containers/home/home.component'
import { ParticipantRegistrationFormComponent } from '@/users/components/participant-registration-form/participant-registration-form.component'
import { AuthGuardService } from '@/users/services/auth.guard.service'


const routes: Routes = [
    {
        path: '',
        children: [
            {
                path: 'user', component: HomeComponent, canActivate: [ AuthGuardService ]
            },
            {
                path: 'user/olymp', component: ParticipantRegistrationFormComponent, canActivate: [ AuthGuardService ]
            }
        ]
    }
]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ],
    providers: [ AuthGuardService ]
} )

export class UsersRoutingModule {}