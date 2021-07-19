import { NgModule } from '@angular/core'
import { ParticipantComponent } from './components/participant/participant.component'
import { HomeComponent } from './containers/home/home.component'
import { UsersRoutingModule } from '@/users/users-routing.module'
import { ParticipantRegistrationFormComponent } from '@/users/components/participant-registration-form/participant-registration-form.component'
import { SharedModule } from '@/shared/shared.module'


const COMPONENTS = [ ParticipantComponent, HomeComponent, ParticipantRegistrationFormComponent ]


@NgModule( {
    declarations: COMPONENTS,
    imports: [
        SharedModule,
        UsersRoutingModule
    ],
    exports: [ UsersRoutingModule ]
} )

export class UsersModule {}
