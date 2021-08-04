import { NgModule } from '@angular/core'
import { ParticipantComponent } from './components/participant/participant.component'
import { HomeComponent } from './containers/home/home.component'
import { UsersRoutingModule } from '@/users/users-routing.module'
import { ParticipantRegistrationFormComponent } from '@/users/components/participant-registration-form/participant-registration-form.component'
import { SharedModule } from '@/shared/shared.module'
import { ParticipantRegistrationFormPersonalComponent } from '@/users/components/participant-registration-form-personal/participant-registration-form-personal.component'
import { ParticipantRegistrationFormEducationComponent } from '@/users/components/participant-registration-form-education/participant-registration-form-education.component'
import { ParticipantCabinetComponent } from '@/users/components/participant-cabinet/participant-cabinet.component'


const COMPONENTS = [
    ParticipantComponent,
    HomeComponent,
    ParticipantRegistrationFormComponent,
    ParticipantRegistrationFormPersonalComponent,
    ParticipantRegistrationFormEducationComponent,
    ParticipantCabinetComponent
]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        UsersRoutingModule
    ],
    exports: [ UsersRoutingModule ]
} )

export class UsersModule {}
