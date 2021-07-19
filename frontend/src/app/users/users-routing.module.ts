import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { HomeComponent } from '@/users/containers/home/home.component'
import { ParticipantRegistrationFormComponent } from '@/users/components/participant-registration-form/participant-registration-form.component'


const routes: Routes = [
    {
        path: '',
        children: [
            { path: 'user', component: HomeComponent },
            { path: 'user/olymp', component: ParticipantRegistrationFormComponent }
        ]
    }
]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )

export class UsersRoutingModule {}