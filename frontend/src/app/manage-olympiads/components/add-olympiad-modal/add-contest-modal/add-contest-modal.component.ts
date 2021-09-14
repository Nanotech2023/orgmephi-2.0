import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core'
import { BaseContest, CreateBaseOlympiadRequestTaskCreator } from '@api/tasks/model'
import SubjectEnum = BaseContest.SubjectEnum


@Component( {
    selector: 'app-add-contest-modal',
    templateUrl: './add-contest-modal.component.html',
    styleUrls: [ './add-contest-modal.component.scss' ],
    host: {
        '(document:click)': 'onClick($event)'
    }
} )
export class AddContestModalComponent
{
    @Input() modalVisible!: boolean
    @Output() modalVisibleChange: EventEmitter<boolean> = new EventEmitter<boolean>()
    @Output() addOlympiad: EventEmitter<CreateBaseOlympiadRequestTaskCreator> = new EventEmitter<CreateBaseOlympiadRequestTaskCreator>()
    @ViewChild( 'modal' ) modal!: ElementRef

    createBaseOlympiadRequestTaskCreator: CreateBaseOlympiadRequestTaskCreator
    isCreated: boolean

    constructor()
    {
        this.createBaseOlympiadRequestTaskCreator = {
            description: '',
            laureate_condition: 0,
            name: '',
            olympiad_type_id: 0,
            rules: '',
            subject: SubjectEnum.Physics,
            target_classes: [],
            winning_condition: 0
        }
        this.isCreated = false
    }

    create(): void
    {
        this.isCreated = true
        this.addOlympiad.emit( this.createBaseOlympiadRequestTaskCreator )
    }

    isValid(): boolean
    {
        return true
    }

    onClick( $event: any ): void
    {
        if ( $event.target == this.modal?.nativeElement )
            this.modalVisible = false
    }
}
