import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { ParticipantCabinetComponent } from '@/profile/components/participant-cabinet/participant-cabinet.component'
import { ParticipantRegistrationFormComponent } from '@/profile/components/participant-registration-form/participant-registration-form.component'
import { AuthGuardService } from '@/shared/auth.guard.service'


const routes: Routes =
    [
        {
            path: 'profile', component: ParticipantCabinetComponent, canActivate: [ AuthGuardService ]
        },
        {
            path: 'profile/edit', component: ParticipantRegistrationFormComponent, canActivate: [ AuthGuardService ]
        }
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class ProfileRoutingModule {}