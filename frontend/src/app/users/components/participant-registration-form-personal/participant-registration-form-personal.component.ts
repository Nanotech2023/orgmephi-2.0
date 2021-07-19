import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { emptyParticipant, Gender, ParticipantRegister } from '@/users/models/participant'
import { ParticipantService } from '@/users/services/participant.service'


@Component( {
    selector: 'app-participant-registration-form-personal',
    templateUrl: './participant-registration-form-personal.component.html',
    styleUrls: [ './participant-registration-form-personal.component.scss' ]
} )
export class ParticipantRegistrationFormPersonalComponent implements OnInit
{

    // @ts-ignore
    @Input() participant: ParticipantRegister
    @Output() participantChange: EventEmitter<ParticipantRegister> = new EventEmitter<ParticipantRegister>()

    genderOptions: Gender[] = [ Gender.male, Gender.female ]
    countriesList: string[] = []

    constructor( private service: ParticipantService )
    {
    }

    ngOnInit(): void
    {
        this.countriesList = this.service.getCountriesList()
    }
}
