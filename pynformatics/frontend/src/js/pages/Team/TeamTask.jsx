import React from 'react';

import Box from '../../components/utility/Box';
import Button from '../../components/utility/Button';
import MainContentWrapper from '../../components/utility/MainContentWrapper';
import {
    gutter,
    colStyle,
    rowStyle,
    Col,
    Row,
} from '../../components/utility/Grid';
import Radio, {RadioGroup} from '../../isomorphic/components/uielements/radio'
import Popconfirm from '../../isomorphic/components/feedback/popconfirm'
import Alert from '../../isomorphic/components/feedback/alert'

export default class TeamTask extends React.Component {
    constructor() {
        super();
    }

    render() {
        const radioStyle = {
            display: 'block',
            height: '30px',
            lineHeight: '30px',
        };
        const text = 'Отправить выбранную команду?';
        //annIcon = <i style={{color: "#ff9d61"}} class="material-icons">announcement</i>

        return (
            <MainContentWrapper>
                <Row>
                    <Alert
                        message="Предупреждение"
                        description="Какое-то предупреждение"
                        type="warning"
                        showIcon
                        closeText="Закрыть"
                    />
                </Row>
                <Box>
                    <Row gutter={gutter} style={rowStyle}>
                        <Col md={12} xs={24} style={colStyle}>
                            <h3>Командный контест</h3>
                            <div style={{ width: '365px', height: '140px', fontSize: '14px'}}>
                                На олимпиаде, в режиме командной олимпиады,
                                три ученика пишут задачи за одним компьютером.
                                Результаты команд хранятся отдельно от результатов учеников.
                                Выберите команду справа или создайте новую.
                            </div>
                            <Button type="primary" size="md">Создать команду</Button>
                        </Col>
                        <Col md={10} xs={12} style={colStyle}>
                            <h4>Выберите команду</h4>
                            <RadioGroup>
                                <Popconfirm placement="bottomLeft" title={text} okText="Да" cancelText="Нет">
                                    <Radio style={radioStyle} value={1}>Вариант 1 (Фамилия, Фамилия, Фамилия)</Radio>
                                </Popconfirm>
                                <Popconfirm placement="bottomLeft" title={text} okText="Да" cancelText="Нет">
                                    <Radio style={radioStyle} value={2}>Вариант 2 (Фамилия, Фамилия, Фамилия)</Radio>
                                </Popconfirm>
                                <Popconfirm placement="bottomLeft" title={text} okText="Да" cancelText="Нет">
                                    <Radio style={radioStyle} value={3}>Вариант 3 (Фамилия, Фамилия, Фамилия)</Radio>
                                </Popconfirm>
                                <Popconfirm placement="bottomLeft" title={text} okText="Да" cancelText="Нет">
                                    <Radio style={radioStyle} value={4}>Вариант 4 (Фамилия, Фамилия, Фамилия)</Radio>
                                </Popconfirm>
                            </RadioGroup>
                            <Button type="primary" size="md">Показать все</Button>
                        </Col>
                    </Row>
                </Box>
            </MainContentWrapper>
        );
    }
}


