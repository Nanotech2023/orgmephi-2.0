import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { ProfileRoutingModule } from '@/profile/profile.routing.module'
import { ParticipantRegistrationFormComponent } from '@/profile/components/participant-registration-form/participant-registration-form.component'
import { ParticipantRegistrationFormPersonalComponent } from '@/profile/components/participant-registration-form-personal/participant-registration-form-personal.component'
import { ParticipantRegistrationFormEducationComponent } from '@/profile/components/participant-registration-form-education/participant-registration-form-education.component'
import { ParticipantCabinetComponent } from '@/profile/components/participant-cabinet/participant-cabinet.component'


const COMPONENTS = [
    ParticipantRegistrationFormComponent,
    ParticipantRegistrationFormPersonalComponent,
    ParticipantRegistrationFormEducationComponent,
    ParticipantCabinetComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        ProfileRoutingModule
    ]
} )
export class ProfileModule {}
