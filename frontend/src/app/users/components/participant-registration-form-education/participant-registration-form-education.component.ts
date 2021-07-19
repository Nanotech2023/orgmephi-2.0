import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { ParticipantRegister } from '@/users/models/participant'


@Component( {
    selector: 'app-participant-registration-form-education',
    templateUrl: './participant-registration-form-education.component.html',
    styleUrls: [ './participant-registration-form-education.component.scss' ]
} )
export class ParticipantRegistrationFormEducationComponent implements OnInit
{


    // @ts-ignore
    @Input() participant: ParticipantRegister
    @Output() participantChange: EventEmitter<ParticipantRegister> = new EventEmitter<ParticipantRegister>()

    constructor() { }

    ngOnInit(): void
    {
    }

}
