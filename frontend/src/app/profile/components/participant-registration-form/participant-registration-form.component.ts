import { Component, OnInit } from '@angular/core'
import { emptyParticipant, ParticipantRegister } from '@/users/models/participant'
import { ParticipantService } from '@/users/services/participant.service'


@Component( {
    selector: 'app-participant-registration-form',
    templateUrl: './participant-registration-form.component.html',
    styleUrls: [ './participant-registration-form.component.scss' ]
} )
export class ParticipantRegistrationFormComponent implements OnInit
{
    // @ts-ignore
    participant: ParticipantRegister
    currentStage: number
    totalStages = 2

    constructor( private service: ParticipantService )
    {
        this.currentStage = 0
    }

    ngOnInit(): void
    {
        this.participant = emptyParticipant
    }
}
