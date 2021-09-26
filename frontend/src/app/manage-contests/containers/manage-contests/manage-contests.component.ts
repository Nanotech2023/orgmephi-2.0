import { Component, OnInit, ViewChild } from '@angular/core'
import { ManageContestsStore } from '@/manage-contests/manage-contests.store'
import { Observable } from 'rxjs'
import { fixedHeight } from '@/shared/consts'
import { User } from '@api/users/models'
import { Contest } from '@api/tasks/model'
import { AgGridAngular } from 'ag-grid-angular'


@Component( {
    selector: 'app-manage-olympiads',
    templateUrl: './manage-contests.component.html',
    styleUrls: [ './manage-contests.component.scss' ],
    providers: [ ManageContestsStore ]
} )
export class ManageContestsComponent implements OnInit
{
    minContainerHeight: number = fixedHeight
    columnDefs = [
        { field: 'contest_id', sortable: true, filter: true, headerName: 'ID' },
        { field: 'description', sortable: true, filter: true, headerName: 'Описание' },
        { field: 'start_time', sortable: true, filter: true, headerName: 'Дата начала' },
        { field: 'end_time', sortable: true, filter: true, headerName: 'Дата окончания' },
        { field: 'rules', sortable: true, filter: true, headerName: 'Правила' },
        { field: 'winning_condition', sortable: true, filter: true, headerName: 'Условия победы' },
        { field: 'laureate_condition', sortable: true, filter: true, headerName: 'Условия лауреата' },
        { field: 'certificate_template', sortable: true, filter: true, headerName: 'Шаблон сертификата' },
        { field: 'visibility', sortable: true, filter: true, headerName: 'Видимость' }
    ]

    contests$: Observable<Contest[]> = this.store.contests$
    addModalVisible: boolean = false
    editModalVisible: boolean = false
    editing: any = null
    @ViewChild( 'table_users' ) agGrid!: AgGridAngular
    
    constructor( private store: ManageContestsStore ) {}

    ngOnInit(): void
    {
        this.store.reload()
    }

    getRowNodeId( data: User ): number | undefined
    {
        return data.id
    }
}
