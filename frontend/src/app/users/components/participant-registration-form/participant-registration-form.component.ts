import { Component, OnInit } from '@angular/core'
import { emptyParticipant, ParticipantRegister } from '@/users/models/participant'


@Component( {
    selector: 'app-participant-registration-form',
    templateUrl: './participant-registration-form.component.html',
    styleUrls: [ './participant-registration-form.component.scss' ]
} )
export class ParticipantRegistrationFormComponent implements OnInit
{

    participant: ParticipantRegister

    constructor()
    {
        this.participant = emptyParticipant
    }

    ngOnInit(): void
    {
    }

}
